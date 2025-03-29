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
    files = get_uploaded_files()
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

        # 生成原始视频记录（保持不变）
        original_name = os.path.splitext(filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        original_video_id = f"{original_name}_{timestamp}"
        user_id = 1

        try:
            conn = pymysql.connect(**mysql_config)
            with conn.cursor() as cursor:
                sql = """INSERT INTO user_videos (video_id, user_id, video_path)
                         VALUES (%s, %s, %s)"""
                cursor.execute(sql, (original_video_id, user_id, input_path))
            conn.commit()
        except Exception as e:
            print(f"数据库错误: {e}")
            return f"Database error: {e}"
        finally:
            conn.close()

        # ⚡ 改为异步处理
        Thread(target=process_video_async, args=(input_path, filename, original_video_id, user_id, mysql_config)).start()

        return redirect(url_for('index'))  # 立即返回页面

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
    # 删除输入视频
    # 获取原始视频ID
    original_name = os.path.splitext(filename)[0]
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # 获取所有相关记录
    try:
        conn = pymysql.connect(**mysql_config)
        with conn.cursor() as cursor:
            # 删除帧记录
            cursor.execute("DELETE FROM video_frames_process WHERE video_id LIKE %s", (f"{original_name}_%",))
            # 删除处理视频记录
            cursor.execute("DELETE FROM user_videos_process WHERE video_id LIKE %s", (f"%{original_name}_%",))
            # 删除原始视频记录
            cursor.execute("DELETE FROM user_videos WHERE video_id LIKE %s", (f"{original_name}_%",))
            conn.commit()
    except Exception as e:
        print(f"数据库删除错误: {e}")
    finally:
        conn.close()

    if os.path.exists(input_path):
        os.remove(input_path)

    # 删除输出视频
    output_path = os.path.join('video/output', filename)
    if os.path.exists(output_path):
        os.remove(output_path)

    # 删除帧目录
    frame_dir = os.path.join('frames', os.path.splitext(filename)[0])
    if os.path.exists(frame_dir):
        for f in os.listdir(frame_dir):
            os.remove(os.path.join(frame_dir, f))
        os.rmdir(frame_dir)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)