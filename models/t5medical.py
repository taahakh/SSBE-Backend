from transformers import pipeline
from model_interface import ModelInterface

class T5MedicalSummarisation(ModelInterface):

    def __init__(self):
        self.pipe = None

    def load_model(self):
        if self.pipe is None:
            print("(T5MedicalSummarisation) Loading model...")
            self.pipe = pipeline("summarization", model="Falconsai/medical_summarization", device=0)
            print("(T5MedicalSummarisation) Model loaded")

    def unload_model(self):
        print("(T5MedicalSummarisation) Unloading model...")
        self.pipe = None
        print("(T5MedicalSummarisation) Model unloaded")

    def summarise(self, text):
        print("(T5MedicalSummarisation) Summarising...")
        return self.pipe(text, min_length=100, max_length=500)[0]['summary_text']
        

