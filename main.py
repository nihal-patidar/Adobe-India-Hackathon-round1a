import pdfplumber
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
import re
import os
from sklearn.metrics import classification_report

# Load model and tokenizer
MODEL_NAME = "local_distilbert_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=4)  # H1, H2, H3, None

# Clean unwanted characters
def clean_text(text):
    text = text.replace('\u0000', '')  # Remove null characters
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)  # Remove other control characters
    return text.strip()

# Classify heading using model
def classify_heading(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class = torch.argmax(logits).item()
    return ["None", "H3", "H2", "H1"][predicted_class]

# Extract headings from PDF
def extract_pdf_headings(pdf_path):
    outline = []
    title = "Unknown Title"

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if not text:
                continue
            text_lines = text.split("\n")
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

# Load ground truth JSON
def load_ground_truth(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Evaluate precision, recall, f1, accuracy
def evaluate_predictions(predicted_outline, ground_truth_data):
    y_true = []
    y_pred = []

    # Build a lookup of ground truth by cleaned text
    if isinstance(ground_truth_data, dict) and "outline" in ground_truth_data:
        ground_truth_data = ground_truth_data["outline"]

    gt_lookup = {clean_text(entry["text"]): entry["level"] for entry in ground_truth_data}

    for item in predicted_outline:
        cleaned_text = clean_text(item["text"])
        pred_label = item["level"]
        true_label = gt_lookup.get(cleaned_text)

        if true_label:
            y_true.append(true_label)
            y_pred.append(pred_label)

    if not y_true:
        print("⚠️ No matches found between predictions and ground truth.")
        return

    print("📊 Evaluation Report:")
    print(classification_report(y_true, y_pred, labels=["H1", "H2", "H3", "None"], zero_division=0))

# Main script
if __name__ == "__main__":
    input_dir = "input"
    output_dir = "output"
    gt_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        filename = os.path.splitext(pdf_file)[0]
        pdf_path = os.path.join(input_dir, pdf_file)
        output_path = os.path.join(output_dir, filename + ".json")
        ground_truth_path = os.path.join(gt_dir, filename + ".json")

        print(f"\n📄 Processing: {pdf_file}")
        result = extract_pdf_headings(pdf_path)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"✅ Saved output to: {output_path}")

        if os.path.exists(ground_truth_path):
            print(f"🔍 Evaluating against ground truth: {ground_truth_path}")
            ground_truth = load_ground_truth(ground_truth_path)
            evaluate_predictions(result["outline"], ground_truth)
        else:
            print("⚠️ Ground truth file not found. Skipping evaluation.")
