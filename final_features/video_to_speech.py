import os
from moviepy.editor import *
from faster_whisper import WhisperModel
import re
from deep_translator import GoogleTranslator
from TTS.api import TTS
import torch

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

def translate_text(transcription, target_language="ar"):
    max_chunk_length = 500
    words = re.findall(r'\b\w+\b', transcription)
    translated_chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) <= max_chunk_length:
            current_chunk += word + " "
        else:
            translated_chunk = GoogleTranslator(source='auto', target=target_language).translate(current_chunk.strip())
            translated_chunks.append(translated_chunk)
            current_chunk = word + " "
    # Translate the last chunk
    if current_chunk:
        translated_chunk = GoogleTranslator(source='auto', target=target_language).translate(current_chunk.strip())
        translated_chunks.append(translated_chunk)
    translated_text = " ".join(translated_chunks)
    return translated_text

# Assuming the function definitions and necessary imports are above this code
# ------> TESTING <------

# def test_processing_pipeline():
#     # Step 0: Input video file path
#     video_path = input("Enter the path of the video file: ")

#     # Step 1: Convert video to audio
#     audio_path = convert_video_to_audio_and_split(video_path)
#     if audio_path:
#         print("Audio file created successfully:", audio_path)
#     else:
#         print("Error occurred during audio conversion.")
#         return

#     # Step 2: Transcribe audio to text
#     transcribed_text = transcribe_audio(audio_path)
#     if transcribed_text:
#         print("Transcription successful:", transcribed_text)
#     else:
#         print("Error occurred during transcription.")
#         return

#     # Step 3: Input target language
#     target_language = input("Enter the target language (e.g., 'ar' for Arabic): ")

#     # Step 4: Translate the transcribed text
#     translated_text = translate_text(transcribed_text, target_language)
#     if translated_text:
#         print("Translation successful:", translated_text)
#     else:
#         print("Error occurred during translation.")
#         return


# # Call the test function
# if __name__ == "__main__":
#     test_processing_pipeline()
