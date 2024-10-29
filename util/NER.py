import spacy
import langid

# Load both English and Russian language models
nlp_en = spacy.load("en_core_web_sm")
nlp_ru = spacy.load("ru_core_news_sm")

def extract_names(text):
    # Detect language using langid
    lang, _ = langid.classify(text)
    
    # Only accept 'en' or 'ru' as valid language codes
    if lang not in ['en', 'ru']:
        lang = 'en'
    
    nlp = nlp_en if lang == "en" else nlp_ru

    # Process text
    doc = nlp(text)
    
    # Initialize result dictionary
    result = {"first_name": "", "middle_name": "", "last_name": "", "full_name": text}
    name_parts = []
    
    # Extract possible names based on token type
    for token in doc:
        if token.ent_type_ == "PERSON" or token.pos_ == "PROPN":
            name_parts.append(token.text)

    # Only proceed if we found name-like tokens
    if name_parts:
        if len(name_parts) == 2:
            result["first_name"], result["last_name"] = name_parts
        elif len(name_parts) == 3:
            result["first_name"], result["middle_name"], result["last_name"] = name_parts
        elif len(name_parts) == 1:
            result["first_name"] = name_parts[0]
        return result
    else:
        return False  # Return False if no name parts were found

# Example usage
text_en = "John Michael Doe"
text_ru = "Иван Иванович Петров"
text_noname = "This is not a name"

# Calling the function and printing outputs
english_output = extract_names(text_en)
russian_output = extract_names(text_ru)
no_name_output = extract_names(text_noname)

print("English:", english_output)  # Should return name structure or False
print("Russian:", russian_output)  # Should return name structure or False
print("No Name:", no_name_output)  # Should return False
