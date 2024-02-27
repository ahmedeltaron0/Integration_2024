import os
from moviepy.editor import *
from faster_whisper import WhisperModel
import re
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import time
from TTS.api import TTS
import torch
from tts_chunks import split_text, check_lang

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

# Define the language dictionary
language = {
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

def translate_text(text,target_language):
    # Prompt the user for the target language
    target_language = input("Enter the target language: ").strip().lower()
    
    # Check if the provided target language is in the language dictionary
    if target_language in language:
        # Get the corresponding language code
        target_language_code = language[target_language]
    else:
        # If not found, use the provided target language as is
        target_language_code = target_language

    max_chunk_length = 500
    words = re.findall(r'\b\w+\b', text)
    translated_chunks = []
    current_chunk = ""
    
    for word in words:
        if len(current_chunk) + len(word) <= max_chunk_length:
            current_chunk += word + " "
        else:
            # Translate using the obtained or provided target language code
            translated_chunk = GoogleTranslator(source='auto', target=target_language_code).translate(current_chunk.strip())
            translated_chunks.append(translated_chunk)
            current_chunk = word + " "
    
    # Translate the last chunk
    if current_chunk:
        # Translate using the obtained or provided target language code
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



#------> TESTING <------
def test_audio_processing():
    # Prompt the user for input audio file path
    input_audio_path = input("Enter the path to the input audio file: ")

    # Prompt the user for clone audio file path
    clone_audio_path = input("Enter the path to the clone audio file: ")
    
    # Prompt the user for input language
    input_lang = input("Enter the input language (e.g., 'en' for English): ")

    # Prompt the user for target language
    target_lang = input("Enter the target language (e.g., 'ar' for Arabic): ")
    
    # Step 1: Convert audio file to WAV
    wav_audio_path = convert_audio_to_wav(input_audio_path)
    
    if wav_audio_path:
        # Step 2: Transcribe audio to text
        transcribed_text = transcribe_audio(wav_audio_path)
        
        if transcribed_text:
            # Step 3: Translate transcribed text
            translated_text = translate_text(transcribed_text, target_lang)
            
            if translated_text:
                # Step 4: Generate speech from translated text
                output_audio_path = generate_speech(input_lang, translated_text, clone_audio_path)
                print("Output audio file:", output_audio_path)
            else:
                print("Translation failed.")
        else:
            print("Transcription failed.")
    else:
        print("Audio conversion failed.")

# Test the audio processing function
test_audio_processing()