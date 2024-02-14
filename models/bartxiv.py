from model_interface import ModelInterface
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class BartXIV(ModelInterface):

    def __init__(self):
        self.tokenizer = None
        self.model = None

    def load_model(self):
        if (self.tokenizer is None) and (self.model is None):
            print("(BartXIV) Loading model...")
            self.tokenizer = AutoTokenizer.from_pretrained("kworts/BARTxiv")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("kworts/BARTxiv")
            print("(BartXIV) Model loaded")

    def unload_model(self):
        print("(BartXIV) Unloading model...")
        self.tokenizer = None
        self.model = None
        print("(BartXIV) Model unloaded")
    
    def summarise(self, text):
        print("(BartXIV) Summarising...")
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model.generate(inputs["input_ids"], num_beams=4, min_length=100, max_length=500)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        
