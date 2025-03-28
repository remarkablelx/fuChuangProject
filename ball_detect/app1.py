import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pymysql
from datetime import datetime
from pymysql import MySQLError
from werkzeug.exceptions import InternalServerError


# 数据库配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'lx20040622',
    'database': 'fwwb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**MYSQL_CONFIG)

def generate_video_id(filename):
    """生成视频ID：文件名+时间戳"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_name = os.path.splitext(filename)[0]
    return f"{base_name}_{timestamp}"

def save_to_database(table_name, data):
    """通用数据库插入函数"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

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


@app.errorhandler(MySQLError)
def handle_mysql_error(e):
    return f"Database error occurred: {str(e)}", 500

@app.errorhandler(InternalServerError)
def handle_internal_error(e):
    return "Internal server error", 500

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
        try:
            # 生成唯一ID和路径
            filename = secure_filename(file.filename)
            video_id = generate_video_id(filename)
            user_id = 1  # 默认用户ID

            # 保存原始视频信息到user_videos
            original_path = os.path.join('video/input', filename)
            video_data = {
                'video_id': video_id,
                'user_id': user_id,
                'video_path': original_path
            }
            save_to_database('user_videos', video_data)

            # 保存文件到本地
            file.save(original_path)

            # 处理视频（保持原有处理逻辑）
            output_path = os.path.join('video/output', filename)
            cmd = [
                'python', 'balldetect_pos_vel/ball_detect.py',
                '--model_path', 'balldetect_pos_vel/ball_detect.pt',
                '--video_path', original_path,
                '--video_out_path', output_path
            ]
            subprocess.run(cmd)

            # 保存处理后视频信息到user_videos_process
            process_data = {
                'video_id': video_id,
                'user_id': user_id,
                'video_path_process': output_path
            }
            save_to_database('user_videos_process', process_data)

            # 处理帧信息
            frame_dir = os.path.join('frames', os.path.splitext(filename)[0])
            frame_files = sorted(os.listdir(frame_dir))

            for idx, frame_file in enumerate(frame_files):
                frame_path = os.path.join(frame_dir, frame_file)
                frame_id = f"{video_id}_{str(idx).zfill(6)}"

                frame_data = {
                    'frame_id': frame_id,
                    'video_id': video_id,
                    'frame_index': idx,
                    'frame_path_process': frame_path
                }
                save_to_database('video_frames_process', frame_data)

            return redirect(url_for('index'))

        except Exception as e:
            return f"Error occurred: {str(e)}", 500

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
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
    # 验证数据库连接
    try:
        conn = get_db_connection()
        print("Successfully connected to database!")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        exit(1)

    app.run(debug=True)