import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import pymysql
from datetime import datetime
from threading import Thread
from models import process_video_async


mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'lx20040622',
    'database': 'fwwb'
}

# Status constants (add to top of app.py)
STATUS_UPLOADED = 1
STATUS_PROCESSING = 2
STATUS_COMPLETED = 3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'video/input'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

# 初始化目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('video/output', exist_ok=True)
os.makedirs('frames', exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_uploaded_files():
    return [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]

@app.route('/')
def index():
    files = []
    try:
        conn = pymysql.connect(**mysql_config)
        with conn.cursor() as cursor:
            sql = """
            SELECT v.video_id, v.video_path, s.status 
            FROM user_videos v
            JOIN video_status s ON v.video_id = s.video_id
            ORDER BY v.video_id DESC
            """
            cursor.execute(sql)
            files = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"数据库查询错误: {e}")

    return render_template('upload.html', files=files)

@app.route('/api/processed_files')
def get_processed_files():
    output_files = os.listdir('video/output')
    return jsonify(output_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # 生成原始视频记录
        original_name = os.path.splitext(filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        original_video_id = f"{original_name}_{timestamp}"
        user_id = 1

        try:
            conn = pymysql.connect(**mysql_config)
            with conn.cursor() as cursor:
                # 插入视频记录
                sql = """INSERT INTO user_videos (video_id, user_id, video_path)
                         VALUES (%s, %s, %s)"""
                cursor.execute(sql, (original_video_id, user_id, input_path))

                # 插入状态记录
                sql = """INSERT INTO video_status (video_id, status)
                         VALUES (%s, %s)"""
                cursor.execute(sql, (original_video_id, STATUS_UPLOADED))

            conn.commit()
        except Exception as e:
            print(f"数据库错误: {e}")
            return f"Database error: {e}"
        finally:
            conn.close()

        return redirect(url_for('index'))

    return redirect(request.url)





# 添加以下三个路由
@app.route('/video/input/<filename>')
def serve_input_video(filename):
    return send_from_directory('video/input', filename)

@app.route('/video/output/<filename>')
def serve_output_video(filename):
    return send_from_directory('video/output', filename)

@app.route('/frames/<path:subpath>')
def serve_frames(subpath):
    return send_from_directory('frames', subpath)

@app.route('/result/<filename>')
def show_result(filename):
    return render_template('result.html',
                          original_video=url_for('serve_input_video', filename=filename),
                          processed_video=url_for('serve_output_video', filename=filename),
                          filename=filename)


@app.route('/frames/<filename>')
@app.route('/frames/<filename>')
def show_frames(filename):
    frame_dir = os.path.join('frames', os.path.splitext(filename)[0])
    if not os.path.exists(frame_dir):
        return "Frames not found", 404

    frames = sorted(os.listdir(frame_dir))
    total_frames = len(frames)

    return render_template('frames.html',
                           frames=[url_for('serve_frames', subpath=f"{os.path.splitext(filename)[0]}/{f}") for f in
                                   frames],
                           filename=filename,
                           total_frames=total_frames)


@app.route('/delete/<filename>')
def delete_file(filename):
    # First, find the exact video_id for this filename
    try:
        conn = pymysql.connect(**mysql_config)
        with conn.cursor() as cursor:
            # Get the exact video_id for this specific file
            sql = "SELECT video_id FROM user_videos WHERE video_path LIKE %s"
            cursor.execute(sql, (f"%{filename}"))
            result = cursor.fetchone()

            if not result:
                print(f"Video not found: {filename}")
                return redirect(url_for('index'))

            video_id = result[0]

            # Now delete using the exact video_id
            cursor.execute("DELETE FROM video_frames_process WHERE video_id = %s", (video_id,))
            cursor.execute("DELETE FROM user_videos_process WHERE video_id LIKE %s", (f"%{video_id.split('_')[-1]}",))
            cursor.execute("DELETE FROM video_status WHERE video_id = %s", (video_id,))
            cursor.execute("DELETE FROM user_videos WHERE video_id = %s", (video_id,))

            conn.commit()
    except Exception as e:
        print(f"数据库删除错误: {e}")
    finally:
        conn.close()

    # Delete the files
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(input_path):
        os.remove(input_path)

    # Delete output video
    output_path = os.path.join('video/output', filename)
    if os.path.exists(output_path):
        os.remove(output_path)

    # Delete frames directory
    frame_dir = os.path.join('frames', os.path.splitext(filename)[0])
    if os.path.exists(frame_dir):
        for f in os.listdir(frame_dir):
            os.remove(os.path.join(frame_dir, f))
        os.rmdir(frame_dir)

    return redirect(url_for('index'))


@app.route('/process/<video_id>')
def process_video(video_id):
    try:
        # 获取视频信息
        conn = pymysql.connect(**mysql_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT video_path FROM user_videos WHERE video_id = %s", (video_id,))
            result = cursor.fetchone()
            if not result:
                return "Video not found", 404

            input_path = result[0]
            filename = os.path.basename(input_path)

            # 更新状态为处理中
            cursor.execute("UPDATE video_status SET status = %s WHERE video_id = %s",
                           (STATUS_PROCESSING, video_id))
        conn.commit()
        conn.close()

        # 启动异步处理
        user_id = 1  # 默认用户ID
        Thread(target=process_video_async,
               args=(input_path, filename, video_id, user_id, mysql_config)).start()

        return redirect(url_for('index'))
    except Exception as e:
        print(f"处理错误: {e}")
        return f"Processing error: {e}"


@app.route('/api/video_status/<video_id>')
def get_video_status(video_id):
    try:
        conn = pymysql.connect(**mysql_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT status FROM video_status WHERE video_id = %s", (video_id,))
            result = cursor.fetchone()
            if not result:
                return jsonify({"error": "Video not found"}), 404
            status = result[0]
        conn.close()
        return jsonify({"status": status})
    except Exception as e:
        print(f"Status query error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)