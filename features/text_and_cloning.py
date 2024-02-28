import os
from TTS.api import TTS
import torch
from pydub import AudioSegment
from tts_chunks import split_text,check_lang
import time

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def generate_speech(input_lang, input_text, input_audio):
    start_time = time.time()
    
    # Check language
    lang = check_lang(input_lang)
    if lang is None:
        raise ValueError(f"Invalid language input: {input_lang}")

    
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
    output_file_path = r"E:\Integration_2024\output\audio\output_All_combined.wav"
    output_audio.export(output_file_path, format="wav")
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time)
    
    return output_file_path

