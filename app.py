from flask import Flask, render_template, request, send_file
from backend.features.video_preprocessing import convert_video_to_audio_and_split
from backend.features.trans import transcribe_audio, translate_text
from backend.features.text_and_cloning import generate_speech
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), OUTPUT_FOLDER, 'text')

def process_video(video_file_path, audio_file_path):
    audio_path = convert_video_to_audio_and_split(video_file_path)
    if audio_path:
        # Transcribe audio
        transcription = transcribe_audio(audio_path)
        transcription_output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'text_transcription_output.txt')
        with open(transcription_output_path, "w", encoding="utf-8") as output_file:
            output_file.write(transcription)
        
        # Translate transcription
        translated_result = translate_text(transcription)
        translation_output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'text_translation_output.txt')
        with open(translation_output_path, "w", encoding="utf-8") as output_file:
            output_file.write(translated_result)

        # Generate speech
        output_audio_path = os.path.join(os.getcwd(), OUTPUT_FOLDER, 'audio', 'tested', 'cloning.wav')
        speaker_wav = audio_file_path
        language = "ar"
        generate_speech(translation_output_path, output_audio_path, speaker_wav, language)

        return transcription_output_path, translation_output_path, output_audio_path
    else:
        return None, None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def upload_file():
    if 'video_file' not in request.files or 'audio_file' not in request.files:
        return 'No file part'

    video_file = request.files['video_file']
    audio_file = request.files['audio_file']
    
    if video_file.filename == '' or audio_file.filename == '':
        return 'No selected file'

    if video_file and audio_file:
        video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        video_file.save(video_file_path)
        audio_file.save(audio_file_path)

        transcription_output_path, translation_output_path, output_audio_path = process_video(video_file_path, audio_file_path)
        if transcription_output_path and translation_output_path and output_audio_path:
            return f'Processing complete. Transcribed text saved to: {transcription_output_path}<br>Translated text saved to: {translation_output_path}<br>Speech generated and saved to: {output_audio_path}'
        else:
            return 'Failed to process video.'

if __name__ == '__main__':
    app.run(debug=True)
