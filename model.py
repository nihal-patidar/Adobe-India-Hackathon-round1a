from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "distilbert-base-multilingual-cased"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=4)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model.save_pretrained("local_distilbert_model")
tokenizer.save_pretrained("local_distilbert_model")