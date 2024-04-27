from model_interface import ModelInterface, SummaryType, TextType
from transformers import *
from summarizer import Summarizer
# from chunker import ChunkedSummarizer

class Model(ModelInterface):

    def __init__(self):
        self.config = None
        self.tokenizer = None
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
        return [TextType.SCIENTIFIC]
    
    @property
    def defined_tokenizer(self):
        return self.tokenizer
    
    @property
    def defined_model(self):
        return self.model

    # Little description about the model
    @property
    def description(self) -> str:
        return "Good for all scientific text"

    @property
    def model_name(self):
        return 'SciBERT'

    def load_model(self):
        if (self.model is None) or (self.tokenizer is None) or (self.config is None):
            print("(SciBERT) Loading model...")
            self.config = AutoConfig.from_pretrained('allenai/scibert_scivocab_uncased')
            self.config.output_hidden_states = True
            self.tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
            self.model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased', config=self.config)
            print("(SciBERT) Model loaded")

    def unload_model(self):
        print("(SciBERT) Unloading model...")
        self.config = None
        self.tokenizer = None
        self.model = None
        print("(SciBERT) Model unloaded")

    @ModelInterface.catch_exception
    def summarise(self, text, summary_length):
        print("(SciBERT) Summarising...")
        print(summary_length)
        length = self.maximum_summary_length
        print(summary_length, length)
        if summary_length != "":
            length = float(summary_length)
        print(summary_length, length)
        model = Summarizer(custom_model=self.model, custom_tokenizer=self.tokenizer)
        return model(text, ratio=length, min_length=10, max_length=200)
