from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Load the multilingual NER model and specify SentencePiece tokenizer
model_name = "Davlan/xlm-roberta-base-ner-hrl"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  # Force use of SentencePiece tokenizer
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Initialize the NER pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

def detect_name(input_name):
    # Use the pipeline to identify entities
    ner_results = ner_pipeline(input_name)

    # Initialize output variables
    first_name = ""
    middle_name = ""
    last_name = ""
    full_name = ""

    # Process the NER results to extract the names
    person_entities = [res for res in ner_results if res['entity'].startswith("B-PER") or res['entity'].startswith("I-PER")]
    
    if person_entities:
        # Reconstruct the full name from detected person entities
        full_name = " ".join([entity['word'] for entity in person_entities])

        # Split the full name into parts (assuming first, middle, and last name)
        name_parts = full_name.split()

        if len(name_parts) > 0:
            first_name = name_parts[0]
        if len(name_parts) > 2:
            middle_name = name_parts[1]
        if len(name_parts) > 1:
            last_name = name_parts[-1]

    return {
        "full_name": full_name if full_name else None,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
    }

# Example Usage
names_to_test = [
    "john smith",
    "Иван Иванович Иванов",
    "Иван",
    "smith",
    "Иванович"
]

for name in names_to_test:
    result = detect_name(name)
    print(f"Input: {name}\nResult: {result}\n")
