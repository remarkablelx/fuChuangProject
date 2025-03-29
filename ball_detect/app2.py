import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

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

        # 处理视频
        output_path = os.path.join('video/output', filename)
        print(output_path)
        cmd = [
            'python', 'balldetect_pos_vel/ball_detect.py',
            '--model_path', 'balldetect_pos_vel/ball_detect.pt',
            '--video_path', input_path,
            '--video_out_path', output_path
        ]
        print(f"执行视频处理命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print(f"视频处理返回码: {result.returncode}")

        if result.returncode != 0:
            return f"Error processing video: {result.stderr}"

        # 提取帧
        frame_output_dir = os.path.join('frames', os.path.splitext(filename)[0])
        print(frame_output_dir)
        os.makedirs(frame_output_dir, exist_ok=True)

        frame_script = [
            'python', 'balldetect_pos_vel/video2frame.py',
            '--video_path', output_path,
            '--output_dir', frame_output_dir,
            '--frame_interval', '1'
        ]
        # 修改帧提取部分
        print(f"执行帧提取命令: {' '.join(frame_script)}")
        frame_result = subprocess.run(frame_script, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print(f"帧提取返回码: {frame_result.returncode}")
        print(f"帧提取输出: {frame_result.stdout[:500]}")
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
    app.run(debug=True)