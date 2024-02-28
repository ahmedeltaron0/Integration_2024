from flask import Flask, render_template, request, url_for,send_from_directory
from moviepy.editor import *
from features.video_to_speech import test_processing_pipeline
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), OUTPUT_FOLDER, 'text')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video/', methods=['GET', 'POST'])
def process():
    video_url = audio_url = output_audio_url = None

    if request.method == 'POST':
        # Check for video file in the uploaded files
        video_file = request.files.get('video_file')
        if video_file and video_file.filename:
            video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
            video_file.save(video_file_path)
            video_url = url_for('uploaded_file', filename=video_file.filename)
        
        # Handle optional audio file upload
        audio_file = request.files.get('audio_file')
        if audio_file and audio_file.filename:
            audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            audio_file.save(audio_file_path)
            audio_url = url_for('uploaded_file', filename=audio_file.filename)
        
        target_language = request.form.get('target_language')
        
        # Call your processing pipeline with the video and optional audio file
        # Assume the result is the path to the processed output audio
        # For demonstration, using audio_file_path as the processed result
        output_audio_path = test_processing_pipeline(video_file_path, target_language, audio_file_path)
        if output_audio_path:
            output_audio_url = url_for('uploaded_file', filename=os.path.basename(output_audio_path))
        
        return render_template('video.html', video_url=video_url, audio_url=audio_url, output_audio_url=output_audio_url)

    return render_template('video.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/audio')
def page2():
    return render_template('audio.html')

@app.route('/text')
def page3():
    return render_template('text.html')

if __name__ == '__main__':
    app.run(debug=True)
