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


