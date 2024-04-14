from model_interface import ModelInterface, SummaryType, TextType
from transformers import *
from summarizer.sbert import SBertSummarizer

class Model(ModelInterface):

    def __init__(self):
        self.model = None

    @property
    def minimum_summary_length(self) -> int:
        return -1

    @property
    def maximum_summary_length(self) -> int:
        return 1

    @property
    def summary_type(self) -> SummaryType:
        return SummaryType.EXTRACTIVE
    
    @property
    def text_type(self) -> list[TextType]:
        return [TextType.GENERAL, TextType.NEWS, TextType.FINANCIAL, TextType.MEDICAL, TextType.SCIENTIFIC]
    
    @property
    def defined_tokenizer(self):
        return None
    
    @property
    def defined_model(self):
        return self.model

    # Little description about the model
    @property
    def description(self) -> str:
        return "Good for all texts"

    @property
    def model_name(self):
        return 'SBERT'

    def load_model(self):
        if self.model is None:
            print("(SBERT) Loading model...")
            self.model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
            print("(SBERT) Model loaded")

    def unload_model(self):
        print("(SBERT) Unloading model...")
        self.model = None
        print("(SBERT) Model unloaded")

    @ModelInterface.catch_exception
    def summarise(self, text, summary_length):
        print("(SBERT) Summarising...")
        print(summary_length)
        length = self.maximum_summary_length
        print(summary_length, length)
        if summary_length != "":
            length = float(summary_length)
        print(summary_length, length)
        return self.model(text, ratio=length, min_length=10, max_length=200)