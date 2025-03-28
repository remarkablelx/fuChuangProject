import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pymysql
from datetime import datetime

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
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 精确到毫秒
        original_video_id = f"{original_name}_{timestamp}"
        user_id = 1

        # 数据库操作（原始视频）
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

        # 处理视频
        output_path = os.path.join('video/output', filename)
        cmd = [
            'python', 'balldetect_pos_vel/ball_detect.py',
            '--model_path', 'balldetect_pos_vel/ball_detect.pt',
            '--video_path', input_path,
            '--video_out_path', output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

        if result.returncode != 0:
            return f"Error processing video: {result.stderr}"

        # 生成处理后的视频记录
        processed_video_id = f"{user_id}_{original_name}_{timestamp}"

        # 数据库操作（处理视频）
        try:
            conn = pymysql.connect(**mysql_config)
            with conn.cursor() as cursor:
                sql = """INSERT INTO user_videos_process (video_id, user_id, video_path_process)
                         VALUES (%s, %s, %s)"""
                cursor.execute(sql, (processed_video_id, user_id, output_path))
            conn.commit()
        except Exception as e:
            print(f"数据库错误: {e}")
            return f"Database error: {e}"
        finally:
            conn.close()

        # 提取帧
        frame_output_dir = os.path.join('frames', os.path.splitext(filename)[0])
        os.makedirs(frame_output_dir, exist_ok=True)

        frame_script = [
            'python', 'balldetect_pos_vel/video2frame.py',
            '--video_path', output_path,
            '--output_dir', frame_output_dir,
            '--frame_interval', '1'
        ]
        frame_result = subprocess.run(frame_script, capture_output=True, text=True, encoding='utf-8', errors='ignore')

        # 生成帧记录
        frame_files = sorted(os.listdir(frame_output_dir))
        for idx, frame_file in enumerate(frame_files, 1):
            frame_path = os.path.join(frame_output_dir, frame_file)
            frame_id = f"{original_name}_{timestamp}_{idx}"

            # 数据库操作（帧记录）
            try:
                conn = pymysql.connect(**mysql_config)
                with conn.cursor() as cursor:
                    sql = """INSERT INTO video_frames_process (frame_id, video_id, frame_index, frame_path_process)
                             VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (frame_id, original_video_id, idx, frame_path))
                conn.commit()
            except Exception as e:
                print(f"帧记录错误: {e}")
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