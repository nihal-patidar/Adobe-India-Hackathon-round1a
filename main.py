import pdfplumber
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
import re

# Load the model and tokenizer
MODEL_NAME = "local_distilbert_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=4)  # H1, H2, H3, None

# Dummy classifier: Replace this with fine-tuned logic or heuristic
def classify_heading(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class = torch.argmax(logits).item()
    return ["None", "H3", "H2", "H1"][predicted_class]

# Score heuristically (optional boost for style)
def heuristic_score(text):
    score = 0
    if len(text.split()) < 6: score += 1
    if text.isupper(): score += 1
    if text.istitle(): score += 1
    return score

# Clean unwanted characters
def clean_text(text):
    text = text.replace('\u0000', '')  # Remove null characters
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)  # Remove other control characters
    return text.strip()

# Extract PDF structure
def extract_pdf_headings(pdf_path):
    outline = []
    title = "Unknown Title"

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text_lines = page.extract_text().split("\n")
            for line in text_lines:
                line = clean_text(line)
                if not line or len(line) > 100:
                    continue

                label = classify_heading(line)
                if label == "H1" and title == "Unknown Title":
                    title = line
                if label != "None":
                    outline.append({
                        "level": label,
                        "text": line,
                        "page": page_num
                    })

    return {
        "title": title,
        "outline": outline
    }

# Main entry
if __name__ == "__main__":
    pdf_path = "input/hindi.pdf"  # 👈 change this to your local PDF path
    result = extract_pdf_headings(pdf_path)

    output_path = "output/output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
