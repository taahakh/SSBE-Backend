from model_interface import ModelInterface, SummaryType, TextType
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# class BartXIV(ModelInterface):
class Model(ModelInterface):

    def __init__(self):
        self.tokenizer = None
        self.model = None
    
    @property
    def minimum_summary_length(self) -> int:
        return 50

    @property
    def maximum_summary_length(self) -> int:
        return 500

    # Abstractive (ab) / Extractive (ex)
    @property
    def summary_type(self) -> SummaryType:
        return SummaryType.ABSTRACTIVE
    
    @property
    def text_type(self) -> list[TextType]:
        return [TextType.SCIENTIFIC]

    # Little description about the model
    @property
    def description(self) -> str:
        return "Good for scientific texts such the journals in arXiv"

    @property
    def model_name(self) -> str:
        return 'BartXIV'

    def load_model(self) -> None:
        if (self.tokenizer is None) and (self.model is None):
            print("(BartXIV) Loading model...")
            self.tokenizer = AutoTokenizer.from_pretrained("kworts/BARTxiv")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("kworts/BARTxiv")
            print("(BartXIV) Model loaded")

    def unload_model(self) -> None:
        print("(BartXIV) Unloading model...")
        self.tokenizer = None
        self.model = None
        print("(BartXIV) Model unloaded")
    
    @ModelInterface.catch_exception
    def summarise(self, text) -> str:
        print("(BartXIV) Summarising...")
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model.generate(inputs["input_ids"], num_beams=4, min_length=100, max_length=500)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        
