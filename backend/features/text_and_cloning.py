from TTS.api import TTS
import torch

def generate_speech(file_path, output_file_path, speaker_wav, language):
    # Read text from file
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Initialize TTS with GPU support
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    # Generate speech
    tts.tts_to_file(text=text,
                    file_path=output_file_path,
                    speaker_wav=speaker_wav,
                    language=language)

def main():
    text_file_path = r"E:\Integration_2024\output\text\text_translation_output.txt"
    output_file_path = r"E:\Integration_2024\output\audio\tested\cloning.wav"
    speaker_wav = r"E:\Integration_2024\backend\static\uploads\hager.wav"
    language = "ar"
    
    generate_speech(text_file_path, output_file_path, speaker_wav, language)
    print("Speech generated and saved to:", output_file_path)

if __name__ == "__main__":
    main()
