from TTS.api import TTS
import torch
# Initialize TTS with GPU support
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
# Set the device to CUDA

# Generate speech by cloning a voice using default settings
tts.tts_to_file(text='''
I wanted to work in think when I was young. I love Egypt. Sisi is my role model in life. I am happy. He is the president of Egypt. The Faculty of Artificial Intelligence is one of the best colleges in Egypt.
''',
                file_path="output_moo.wav",
                speaker_wav="1.wav",
                language="en")