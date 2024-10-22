import spacy
import re

# Load models for English and Russian
nlp_en = spacy.load("en_core_web_sm")
nlp_ru = spacy.load("ru_core_news_sm")  # You can try 'ru_core_news_md' or 'ru_core_news_lg' for better performance

# Regex to identify basic name patterns (fallback for Russian names if NER fails)
name_pattern = re.compile(r'^[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)*$')

def detect_name(text, lang='en'):
    # Choose the correct model based on language
    nlp = nlp_en if lang == 'en' else nlp_ru
    
    # Process the text with the chosen model
    doc = nlp(text)
    
    # Extract names with NER
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
    # If NER does not find any Russian name, fallback to regex check
    if lang == 'ru' and not names:
        if name_pattern.match(text):
            names = text.split()
    
    # Determine type of name
    if len(names) == 1:
        return {"Full Name": names[0]}
    elif len(names) > 1:
        return {"First Name": names[0], "Surname": names[-1]}
    return False

# Example usage
print(detect_name("John Smith", 'en'))     # English name
print(detect_name("Иван Иванович Иванов", 'ru'))  # Russian full name
print(detect_name("Анна", 'ru'))           # Russian first name
