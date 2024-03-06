# from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from model_interface import ModelInterface, SummaryType, TextType
from chunker import ChunkedSummarizer

class CustomCS(ChunkedSummarizer):

    def __init__(self, t, m, max_chunk_length, max_summary_length):
        super().__init__(t, m, max_chunk_length, max_summary_length)
    
    def model_generate(self, input_ids):
        return self.model.generate(input_ids, 
                                   min_length=self.min_summary_length, 
                                   max_length=self.max_summary_length, 
                                   num_beams=4, 
                                   early_stopping=True,
                                   no_repeat_ngram_size=3)

# class T5MedicalSummarisation(ModelInterface):
class Model(ModelInterface):

    def __init__(self):
        self.tokenizer = None
        self.model = None

    @property
    def minimum_summary_length(self) -> int:
        return 40

    @property
    def maximum_summary_length(self) -> int:
        return 512

    # Abstractive (ab) / Extractive (ex)
    @property
    def summary_type(self) -> SummaryType:
        return SummaryType.ABSTRACTIVE
    
    @property
    def text_type(self) -> list[TextType]:
        return [TextType.SCIENTIFIC, TextType.MEDICAL]

    # Little description about the model
    @property
    def description(self) -> str:
        return "Good for medical scientific texts"

    @property
    def model_name(self):
        return 'T5MedicalSummarisation'

    def load_model(self):
        if (self.tokenizer is None) or (self.model is None):
            print("(T5MedicalSummarisation) Loading model...")
            self.tokenizer = AutoTokenizer.from_pretrained("Falconsai/medical_summarization")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/medical_summarization")
            print("(T5MedicalSummarisation) Model loaded")

    def unload_model(self):
        print("(T5MedicalSummarisation) Unloading model...")
        self.tokenizer = None
        self.model = None
        print("(T5MedicalSummarisation) Model unloaded")

    @ModelInterface.catch_exception
    def summarise(self, text, summary_length):
        print("(T5MedicalSummarisation) Summarising...")
        length = self.maximum_summary_length
        if summary_length != "":
            length = int(summary_length)
        chunked_summarizer = CustomCS(t=self.tokenizer, m=self.model, max_chunk_length=512, max_summary_length=length)
        return chunked_summarizer.summarize_chunked_text(text)
        # return self.pipe(text, min_length=100, max_length=500)[0]['summary_text']
        

