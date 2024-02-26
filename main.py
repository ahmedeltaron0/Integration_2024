from backend.features.video_preprocessing import convert_video_to_audio_and_split
from backend.features.trans import transcribe_audio, translate_text
from backend.features.text_and_cloning import generate_speech
import os

def main():
    input_path = input("Enter the path to the video or audio file: ")
    
    if os.path.isfile(input_path):
        _, file_extension = os.path.splitext(input_path)
        
        if file_extension.lower() in ['.mp4', '.mov', '.avi']:  # Video file
            audio_path = convert_video_to_audio_and_split(input_path)
            if audio_path:
                process_audio(audio_path)
            else:
                print("Failed to convert video to audio.")
        elif file_extension.lower() in ['.wav', '.mp3']:  # Audio file
            process_audio(input_path)
        else:
            print("Unsupported file format. Please provide a video or audio file.")
    else:
        print("The specified file does not exist.")

def process_audio(audio_path):
    # Step 2: Transcribe audio
    transcription = transcribe_audio(audio_path)
    transcription_output_path = r"E:\Integration_2024\output\text\text_transcription_output.txt"
    with open(transcription_output_path, "w", encoding="utf-8") as output_file:
        output_file.write(transcription)
    print("Transcription complete. Transcribed text saved to:", transcription_output_path)
    
    # Step 3: Translate transcription
    translated_result = translate_text(transcription)
    translation_output_path = r"E:\Integration_2024\output\text\text_translation_output.txt"
    with open(translation_output_path, "w", encoding="utf-8") as output_file:
        output_file.write(translated_result)
    print("Translation complete. Translated text saved to:", translation_output_path)
    
    # Step 4: Generate speech
    output_audio_path = r"E:\Integration_2024\output\audio\tested\cloning.wav"
    speaker_wav = r"E:\Integration_2024\uploads\hager.wav"
    language = "ar"
    generate_speech(translation_output_path, output_audio_path, speaker_wav, language)
    print("Speech generated and saved to:", output_audio_path)

if __name__ == "__main__":
    main()
