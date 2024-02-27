from flask import Flask, render_template, request
import os
from moviepy.editor import *
from TTS.api import TTS
import torch
from features.video_to_speech import convert_video_to_audio_and_split, transcribe_audio, translate_text, generate_speech
from features.tts_chunks import check_lang

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Language mapping dictionary
language_mapping = {
    "english": 'en',
    "spanish": 'es',
    "french": 'fr', 
    "german": 'de',
    "italian": 'it',
    "portuguese": 'pt',
    "polish": 'pl',
    "turkish": 'tr',
    "russian": "ru",
    "dutch": "nl",
    "czech": "cs",
    "arabic": 'ar',
    "chinese": 'zh',
    "japanese": "ja",
    "hungarian": 'hu',
    "korean": 'ko',
    "hindi": 'hi'
}

@app.route('/video', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        # Get uploaded files and form data
        video_file = request.files['video']
        target_language = request.form['target_language']
        clone_audio_file = request.files['audio']

        # Save uploaded files
        video_path = os.path.join("uploads", video_file.filename)
        video_file.save(video_path)

        clone_audio_path = os.path.join("uploads", clone_audio_file.filename)
        clone_audio_file.save(clone_audio_path)

        # Step 1: Convert video to audio
        audio_path = convert_video_to_audio_and_split(video_path)

        # Step 2: Transcribe audio to text
        transcribed_text = transcribe_audio(audio_path)

        # Step 3: Translate the transcribed text
        translated_text = translate_text(transcribed_text, target_language, language_mapping)

        # Step 4: Generate speech
        output_audio_path = generate_speech(check_lang(target_language), translated_text, clone_audio_path)

        # Provide the output audio file path to the template
        output_audio_filename = os.path.basename(output_audio_path)

        return render_template('result.html', output_audio=output_audio_filename, language_mapping=language_mapping)
    

    return render_template('video.html', language_mapping=language_mapping)

@app.route('/audio')
def page2():
    return render_template('audio.html')

@app.route('/text')
def page3():
    return render_template('text.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
