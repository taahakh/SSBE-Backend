from model_interface import ModelInterface, SummaryType, TextType
from transformers import pipeline

# class BartLargeCNN(ModelInterface):
class Model(ModelInterface):

    def __init__(self):
        self.pipe = None

    @property
    def minimum_summary_length(self) -> int:
        return 60

    @property
    def maximum_summary_length(self) -> int:
        return 500

    # Abstractive (ab) / Extractive (ex)
    @property
    def summary_type(self) -> SummaryType:
        return SummaryType.EXTRACTIVE
    
    @property
    def text_type(self) -> list[TextType]:
        return [TextType.GENERAL, TextType.NEWS, TextType.SCIENTIFIC]

    # Little description about the model
    @property
    def description(self) -> str:
        return "Good for all types of text"

    @property
    def model_name(self):
        return 'DUMMY'

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
        
