from transformers import pipeline
from model_interface import ModelInterface, SummaryType, TextType

# class T5MedicalSummarisation(ModelInterface):
class Model(ModelInterface):

    def __init__(self):
        self.pipe = None

    @property
    def minimum_summary_length(self) -> int:
        return 40

    @property
    def maximum_summary_length(self) -> int:
        return 400

    # Abstractive (ab) / Extractive (ex)
    @property
    def summary_type(self) -> SummaryType:
        return SummaryType.ABSTRACTIVE
    
    @property
    def text_type(self) -> list[TextType]:
        return [TextType.SCIENTIFIC, TextType.SCIENTIFIC]

    # Little description about the model
    @property
    def description(self) -> str:
        return "Good for medical scientific texts"

    @property
    def model_name(self):
        return 'T5MedicalSummarisation'

    def load_model(self):
        if self.pipe is None:
            print("(T5MedicalSummarisation) Loading model...")
            self.pipe = pipeline("summarization", model="Falconsai/medical_summarization", device=0)
            print("(T5MedicalSummarisation) Model loaded")

    def unload_model(self):
        print("(T5MedicalSummarisation) Unloading model...")
        self.pipe = None
        print("(T5MedicalSummarisation) Model unloaded")

    @ModelInterface.catch_exception
    def summarise(self, text):
        print("(T5MedicalSummarisation) Summarising...")
        return self.pipe(text, min_length=100, max_length=500)[0]['summary_text']
        

