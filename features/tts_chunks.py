def split_text(input_text):
    
    chunk_size = 160
    chunks = []
    current_chunk = ""

    for word in input_text.split():
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def check_lang(input_lang='arabic'):
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
        "chinese": 'cn',
        "japanese": "ja",
        "hungarian": 'hu',
        "korean": 'ko',
        "hindi": 'hi'
    }
    print(f"Input language: {input_lang}")  # Debug print

    # Attempt to retrieve the language code from the dictionary
    # If input_lang is not found, default to 'en' (English) or any other valid code
    lang_code = language.get(input_lang.lower(), 'en')  # Default to English if not found

    return lang_code
