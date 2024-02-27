from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

def transcribe_audio(audio_path):
    model = WhisperModel("large-v3", compute_type="float16")
    segments, _ = model.transcribe(audio_path)
    transcriptions = ""
    for segment in segments:
        transcriptions += segment.text + " "
    return transcriptions.strip()

def translate_text(text, target_language="ar"):
    max_chunk_length = 500
    words = text.split()

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
def test_translate_text():
    # Input text to translate
    text_to_translate = input("Enter the text to translate: ")

    # Input target language
    target_language = input("Enter the target language (e.g., 'ar' for Arabic): ")

    # Translate the text
    translated_text = translate_text(text_to_translate, target_language)
    if translated_text:
        print("Translated text:", translated_text)
    else:
        print("Translation failed.")

# Call the test function
if __name__ == "__main__":
    test_translate_text()
