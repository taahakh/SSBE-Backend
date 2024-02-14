# # Load model directly
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("hardikJ11/bart-base-finetuned-cnn-news")
# model = AutoModelForSeq2SeqLM.from_pretrained("hardikJ11/bart-base-finetuned-cnn-news")



# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import models.bartxiv, models.bartlargecnn

tokenizer = AutoTokenizer.from_pretrained("kworts/BARTxiv")
model = AutoModelForSeq2SeqLM.from_pretrained("kworts/BARTxiv")

# m = models.bartxiv.BartXIV()
m = models.bartlargecnn.BartLargeCNN()


def summarise(text):
    m.load_model()
    return m.summarise(text)

# from transformers import pipeline

# pipe = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

# def summarise(text):
#     return pipe(text, min_length=100, max_length=500)[0]['summary_text']



# def summarise(text):
#     inputs = tokenizer(text, return_tensors="pt")
#     outputs = model.generate(inputs["input_ids"], num_beams=4, min_length=100, max_length=500)
#     return tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]






# inputs = tokenizer(input_text, return_tensors="pt")
# outputs = model(**inputs)

# summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=100, max_length=500)
# print(tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])