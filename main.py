from backend.features.video_preprocessing import convert_video_to_audio_and_split
from backend.features.trans import transcribe_audio, translate_text

def main():
        # Step 1: convert audio 
    converted = input("Enter the path to the video file: ")
    audio_path = convert_video_to_audio_and_split(converted)
    if audio_path:
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
    else:
        print("Failed to convert video to audio.")

if __name__ == "__main__":
    main()

