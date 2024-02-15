from model_interface import ModelInterface
from transformers import pipeline

class BartLargeCNN(ModelInterface):

    def __init__(self):
        self.pipe = None

    def load_model(self):
        if self.pipe is None:
            print("(BartLargeCNN) Loading model...")
            self.pipe = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
            print("(BartLargeCNN) Model loaded")

    def unload_model(self):
        print("(BartLargeCNN) Unloading model...")
        self.pipe = None
        print("(BartLargeCNN) Model unloaded")

    @ModelInterface.catch_exception
    def summarise(self, text):
        print("(BartLargeCNN) Summarising...")
        return self.pipe(text, min_length=100, max_length=500)[0]['summary_text']
        
