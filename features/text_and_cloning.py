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

# def test_generate_speech():
#     input_lang = "arabic"
#     input_text = "The quick brown fox jumps over the lazy dog. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris. Integer in mauris eu nibh euismod gravida. Duis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor."
#     input_audio = r"E:\Integration_2024\uploads\hager.wav"
    
#     # Call the function
#     output_file = generate_speech(input_lang, input_text, input_audio)
    
#     # Check if the output file exists
#     if os.path.exists(output_file):
#         print("Speech generated successfully and saved to:", output_file)
#         # Optionally, you can add more assertions to verify the output audio
#     else:
#         print("Error: Speech generation failed.")

# if __name__ == '__main__':
#     test_generate_speech()
