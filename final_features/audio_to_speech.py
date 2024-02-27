import os
from moviepy.editor import *
from faster_whisper import WhisperModel
import re
from deep_translator import GoogleTranslator
from pydub import AudioSegment

# for laptop --> from multiprocessing import freeze_support  # Step 1: Import freeze_support()
def convert_audio_to_wav(local_audio_path):
    # Ensure the output directory exists
    output_directory = r'E:\Integration_2024\uploads'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Construct the output audio file path
    output_audio_path = os.path.join(output_directory, os.path.splitext(os.path.basename(local_audio_path))[0] + '.wav')
    try:
        # Load the audio file
        audio = AudioSegment.from_file(local_audio_path)
        # Export audio to a WAV file
        audio.export(output_audio_path, format="wav")
        print("Audio was successfully converted to WAV")
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
def translate_text(text, target_language="ar"):
    max_chunk_length = 500
    words = re.findall(r'\b\w+\b', text)
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

#------> TESTING <------
# def test_audio_processing():
#     # Step 0: Input audio file path
#     audio_path = input("Enter the path of the audio file: ")

#     # Step 1: Convert audio to WAV
#     wav_audio_path = convert_audio_to_wav(audio_path)
#     if not wav_audio_path:
#         print("Error occurred during audio conversion.")
#         return

#     # Step 2: Transcribe audio to text
#     transcribed_text = transcribe_audio(wav_audio_path)
#     if not transcribed_text:
#         print("Error occurred during transcription.")
#         return
#     print("Transcribed text:", transcribed_text)

#     # Step 3: Input target language
#     target_language = input("Enter the target language (e.g., 'ar' for Arabic): ")

#     # Step 4: Translate the transcribed text
#     translated_text = translate_text(transcribed_text, target_language)
#     if not translated_text:
#         print("Error occurred during translation.")
#         return

#     print("Translated text:", translated_text)


# # Call the test function
# if __name__ == "__main__":
#     test_audio_processing()

