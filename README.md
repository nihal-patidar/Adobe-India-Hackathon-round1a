# 📄 PDF Heading Extractor

Automatically extract structured headings (**H1**, **H2**, **H3**) from PDF documents using a combination of **pdfplumber** and a **fine-tuned DistilBERT model**.

---

## ✨ Overview

This project is designed to convert raw PDF files into a well-organized hierarchy of headings. It detects the structural layout of documents by semantically identifying heading levels using machine learning.

---

## 🛠️ Features

- ✅ **Heading Classification**: Detects and classifies headings as H1, H2, or H3.
- ✅ **Layout-Aware Text Extraction**: Uses `pdfplumber` to respect the spatial layout of the PDF.
- ✅ **BERT-powered Intelligence**: Leverages a fine-tuned DistilBERT model for semantic understanding.
- ✅ **Scalable & Fast**: Lightweight yet robust — ready for large batches of documents.

---

## 🧠 How It Works

1. **PDF Parsing**: `pdfplumber` extracts text blocks with metadata (like font size and position).
2. **Feature Extraction**: Text features (e.g., font size, indentation, text casing) are prepared.
3. **Model Prediction**: A fine-tuned DistilBERT model predicts the heading level (H1, H2, H3).
4. **Structured Output**: Headings are output in a hierarchical structure (e.g., JSON or tree format).

---

## 📦 Tech Stack

| Component       | Description                              |
|-----------------|------------------------------------------|
| **Python**      | Programming Language                     |
| **pdfplumber**  | PDF layout-aware text extraction         |
| **DistilBERT**  | Transformer model for heading detection  |
| **Pandas**      | Data processing and feature engineering  |

---

## 📈 Use Cases

- 🧾 Summarizing large documents
- 📚 Auto-generating Table of Contents
- 🔍 Feeding structured content into NLP pipelines
- 📂 Converting unstructured PDFs into knowledge graphs

---

## 🚀 Why This Approach?

Traditional methods rely heavily on:
- Font sizes
- Boldness
- Spacing

But they **fail** when:
- Styles vary across documents
- PDFs are scanned or poorly formatted

By combining **visual cues** and **semantic understanding**, this project produces **highly accurate** and **human-like** heading classification.

---

Let me know if you'd like a demo snippet, visualization, or integration example added!
