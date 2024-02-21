from faster_whisper import WhisperModel
import os
import re
from deep_translator import GoogleTranslator

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

#if __name__ == "__main__":
    audio_path = r"E:\Integration_2024\output\audio\tested\vocals.wav"
    transcription = transcribe_audio(audio_path)
    transcription_output_path = r"E:\Integration_2024\output\text\text_transcription_output.txt"
    with open(transcription_output_path, "w", encoding="utf-8") as output_file:
        output_file.write(transcription)

    with open(transcription_output_path, "r", encoding="utf-8") as input_file:
        transcription_result = input_file.read()

    translated_result = translate_text(transcription_result)
    translation_output_path = r"E:\Integration_2024\output\text\text_translation_output.txt"
    with open(translation_output_path, "w", encoding="utf-8") as output_file:
        output_file.write(translated_result)

    print("Translation complete. Translated text saved to:", translation_output_path)
