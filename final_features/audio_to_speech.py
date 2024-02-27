import os
from moviepy.editor import *
from faster_whisper import WhisperModel
import re
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import time
from TTS.api import TTS
import torch
from features.tts_chunks import split_text, check_lang

# for laptop --> from multiprocessing import freeze_support  # Step 1: Import freeze_support()

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

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



#------> TESTING <------
def test_audio_processing():
    # Step 0: Input audio file path
    audio_path = input("Enter the path of the audio file: ")

    # Step 1: Convert audio to WAV
    wav_audio_path = convert_audio_to_wav(audio_path)
    if not wav_audio_path:
        print("Error occurred during audio conversion.")
        return

    # Step 2: Transcribe audio to text
    transcribed_text = transcribe_audio(wav_audio_path)
    if not transcribed_text:
        print("Error occurred during transcription.")
        return
    print("Transcribed text:", transcribed_text)

    # Step 3: Input target language
    target_language = input("Enter the target language (e.g., 'ar' for Arabic): ")

    # Step 4: Translate the transcribed text
    translated_text = translate_text(transcribed_text, target_language)
    if not translated_text:
        print("Error occurred during translation.")
        return

    print("Translated text:", translated_text)

    input_lang = input("Enter the target language (e.g., 'ar' for Arabic): ")


    # Step 5: Generate speech
    output_audio_path = generate_speech(input_lang , translated_text, wav_audio_path)
    if not output_audio_path:
        print("Error occurred during speech generation.")
        return

    print("Speech generated successfully and saved to:", output_audio_path)

# Call the test function
if __name__ == "__main__":
    test_audio_processing()
