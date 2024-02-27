import os
from moviepy.editor import *
from faster_whisper import WhisperModel
import re
from deep_translator import GoogleTranslator
from TTS.api import TTS
import torch
from features.tts_chunks import split_text, check_lang
import time
from pydub import AudioSegment

# for laptop --> from multiprocessing import freeze_support  # Step 1: Import freeze_support()

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def convert_video_to_audio_and_split(local_video_path):
    # Ensure the output directory exists
    output_directory = r'E:\Integration_2024\uploads'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Construct the output audio file path
    output_audio_path = os.path.join(output_directory, os.path.splitext(os.path.basename(local_video_path))[0] + '.wav')
    try:
        # Load the video file
        video = VideoFileClip(local_video_path)
        # Extract audio from the video
        audio = video.audio
        # Write the audio to a WAV file
        audio.write_audiofile(output_audio_path)
        # Close the video and audio objects to free resources
        video.close()
        audio.close()
        print("Video was successfully converted to audio")
        return output_audio_path  # Return the output audio path
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None
    
def transcribe_audio(audio_path):
    model = WhisperModel("large-v3", compute_type="float16")
    segments, _ = model.transcribe(audio_path)
    transcriptions = ""
    for segment in segments:
        transcriptions += segment.text + " "
    return transcriptions.strip()

def translate_text(transcription, target_language="ar", language_mapping=None):
    if language_mapping is None:
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
    
    max_chunk_length = 500
    words = re.findall(r'\b\w+\b', transcription)
    translated_chunks = []
    current_chunk = ""
    
    # Map the target language name to its corresponding code if available
    target_language_code = language_mapping.get(target_language.lower(), target_language)
    
    for word in words:
        if len(current_chunk) + len(word) <= max_chunk_length:
            current_chunk += word + " "
        else:
            translated_chunk = GoogleTranslator(source='auto', target=target_language_code).translate(current_chunk.strip())
            translated_chunks.append(translated_chunk)
            current_chunk = word + " "
    
    # Translate the last chunk
    if current_chunk:
        translated_chunk = GoogleTranslator(source='auto', target=target_language_code).translate(current_chunk.strip())
        translated_chunks.append(translated_chunk)
    
    translated_text = " ".join(translated_chunks)
    return translated_text

def generate_speech(input_lang, input_text, input_audio):
    start_time = time.time()
    
    # Check language
    lang = check_lang(input_lang)
    
    # Split text into chunks
    chunks = split_text(input_text)
    
    # Initialize output audio segment
    output_audio = AudioSegment.empty()
    
    # Generate speech for each text chunk
    for chunk in chunks:
        tts.tts_to_file(text=chunk,
                        file_path="output_temp.wav",
                        speaker_wav=input_audio,
                        language=lang)
        chunk_audio = AudioSegment.from_wav("output_temp.wav")
        output_audio += chunk_audio
        
        # Delete the temporary file
        os.remove("output_temp.wav")
    
    # Export the combined audio
    output_file_path = "output_All_combined.wav"
    output_audio.export(output_file_path, format="wav")
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time)
    
    return output_file_path



# ------> TESTING <------


# Assuming the necessary function definitions are available

# Define the test function
def test_processing_pipeline():
    # Step 0: Input video file path
    video_path = input("Enter the path of the video file: ")

    # Step 1: Convert video to audio
    audio_path = convert_video_to_audio_and_split(video_path)
    if audio_path:
        print("Audio file created successfully:", audio_path)
    else:
        print("Error occurred during audio conversion.")
        return

    # Step 2: Transcribe audio to text
    transcribed_text = transcribe_audio(audio_path)
    if transcribed_text:
        print("Transcription successful:", transcribed_text)
    else:
        print("Error occurred during transcription.")
        return

    # Step 3: Input target language
    target_language = input("Enter the target language (e.g., 'ar' for Arabic): ")

    # Step 4: Translate the transcribed text
    translated_text = translate_text(transcribed_text, target_language)
    if translated_text:
        print("Translation successful:", translated_text)
    else:
        print("Error occurred during translation.")
        return
    
    # Step 5: Prompt user for clone audio file path
    clone_audio_path = input("Enter the path to the clone audio file: ")
    
    # Step 6: Generate speech
    output_audio_path = generate_speech(target_language, translated_text, clone_audio_path)
    if output_audio_path:
        print("Speech generated successfully and saved to:", output_audio_path)
    else:
        print("Error occurred during speech generation.")
        return

# Call the test function
if __name__ == "__main__":
    test_processing_pipeline()
