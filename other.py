# # Load model directly
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("hardikJ11/bart-base-finetuned-cnn-news")
# model = AutoModelForSeq2SeqLM.from_pretrained("hardikJ11/bart-base-finetuned-cnn-news")

# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("kworts/BARTxiv")
model = AutoModelForSeq2SeqLM.from_pretrained("kworts/BARTxiv")

input_text = """
Writing in ancient Egypt—both hieroglyphic and hieratic—first appeared in the late 4th millennium BC during the late phase of predynastic Egypt. By the Old Kingdom (26th century BC to 22nd century BC), literary works included funerary texts, epistles and letters, hymns and poems, and commemorative autobiographical texts recounting the careers of prominent administrative officials. It was not until the early Middle Kingdom (21st century BC to 17th century BC) that a narrative Egyptian literature was created. This was a "media revolution" which, according to Richard B. Parkinson, was the result of the rise of an intellectual class of scribes, new cultural sensibilities about individuality, unprecedented levels of literacy, and mainstream access to written materials.[2] The creation of literature was thus an elite exercise, monopolized by a scribal class attached to government offices and the royal court of the ruling pharaoh. However, there is no full consensus among modern scholars concerning the dependence of ancient Egyptian literature on the sociopolitical order of the royal courts.
"""
print("start")

def summarise(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], num_beams=4, min_length=100, max_length=500)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

# inputs = tokenizer(input_text, return_tensors="pt")
# outputs = model(**inputs)

# summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=100, max_length=500)
# print(tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])