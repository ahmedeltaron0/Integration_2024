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

language={  
            "english" :'en',
            "spanish" :'es',
            "french" :'fr', 
            "german": 'de',
            "italian" :'it',
            "portuguese":'pt',
            "polish": 'pl',
            "turkish" :'tr',
            "russian" :"ru",
            "dutch": "nl",
            "czech": "cs",
            "arabic" :'ar',
            "chinese": 'cn',
            "japanese" :"ja",
            "hungarian": 'hu',
            "korean" :'ko',
            "hindi": 'hi'
        }

def check_lang(input_lang):
    lang = None  # Default value
    for key, value in language.items():
        if input_lang.lower() == key:
            lang = value
            break
    return lang