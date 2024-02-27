from deep_translator import GoogleTranslator

def translate_text(text, target_language="ar"):
    try:
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated_text
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None
    
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
