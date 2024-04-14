from model_interface import ModelInterface, SummaryType, TextType
from summa.summarizer import summarize as suma

class Model(ModelInterface):

    def __init__(self):
        self.model = None

    @property
    def minimum_summary_length(self) -> int:
        return -1

    @property
    def maximum_summary_length(self) -> int:
        return 1

    # Abstractive (ab) / Extractive (ex)
    @property
    def summary_type(self) -> SummaryType:
        return SummaryType.EXTRACTIVE
    
    @property
    def text_type(self) -> list[TextType]:
        return [TextType.GENERAL]
    
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
        return 'Summa'

    def load_model(self):
        if self.model is None:
            print("(Summa) Loading model...")
            print("(Summa) Model loaded")

    def unload_model(self):
        print("(Summa) Unloading model...")
        print("(Summa) Model unloaded")

    @ModelInterface.catch_exception
    def summarise(self, text, summary_length):
        print("(Summa) Summarising...")
        print(summary_length)
        length = 0.2
        print(summary_length, length)
        if summary_length != "":
            length = float(summary_length)
        print(summary_length, length)
        return suma(text, ratio=length)