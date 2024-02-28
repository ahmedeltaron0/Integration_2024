from deep_translator import GoogleTranslator
import  re
from TTS.api import TTS
import torch

# for laptop --> from multiprocessing import freeze_support  # Step 1: Import freeze_support()

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

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
    
#------> TESTING <------
    
def test_translation():
    # Step 1: Input text to translate
    text_to_translate = input("Enter the text to translate: ")

    # Step 2: Input target language
    target_language = input("Enter the target language (e.g., 'fr' for French): ")

    # Step 3: Translate the text
    translated_text = translate_text(text_to_translate, target_language)
    if translated_text:
        print("Translated text:", translated_text)
    else:
        print("Error occurred during translation.")
    

# Call the test function
if __name__ == "__main__":
    test_translation()
