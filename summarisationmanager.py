import importlib
import json
import os

from model_interface import SummaryType

class SummarisationManager:

    def __init__(self, model_src_path='model_list.txt', json_output_path='md.json'):
        self.model_list = {}
        self.curr_loaded_model = None;
        
        if (not self.load_resources(model_src_path)):
            print("Failed to load resources")
            exit(1)

        self.create_model_descriptors(json_output_path)

    def create_model_descriptors(self, output_path):
        
        descriptor_list = []

        for _, value in self.model_list.items():
            if value.summary_type.value == "Abstractive": 
                st = "ab" 
            else:
                st = "ex"

            model_descriptor = {
                "model-name" : value.model_name,
                "text-type" : [x.value for x in value.text_type],
                "summary-type" : st,
                "description" : value.description,
                "summary-length" : {
                    "min" : value.minimum_summary_length, 
                    "max" : value.maximum_summary_length
                }
            }
        
            descriptor_list.append(model_descriptor)
        
        with open(output_path, 'w') as file:
            json.dump(descriptor_list, file, indent=2)


    def load_resources(self, src_path) -> bool:

        if src_path is None or src_path == "":
            return False
        
        if os.path.getsize(src_path) == 0:
            return False

        with open(src_path, 'r') as file:
            model_list = file.read().splitlines()
            print(model_list)

        try:
            for model in model_list:
                model = importlib.import_module("models."+model)
                self.model_list[model.Model().model_name] = model.Model()
        except Exception as e:
            print(e)
            print("Model name not found in models directory")
            return False
        
        return True

    def model_loader(self, model):
        if self.curr_loaded_model is not None:
            self.curr_loaded_model.unload_model()
        if model not in self.model_list:
            return False, None
        m = self.model_list[model]
        m.load_model()
        self.curr_loaded_model = m
        return True, m
    
    def is_model_abstractive(self, model_name):
        if model_name not in self.model_list:
            return None
        return self.model_list[model_name] if self.model_list[model_name].summary_type == SummaryType.ABSTRACTIVE else None
        
    def summarise(self, text, model_name, summary_length):
        print("Loading Model...")
        exist, model = self.model_loader(model_name)

        if not exist:
            print("Model not found")
            return exist, None

        print("Model Loaded")
        print("Summarising...") 
        return model.summarise(text, summary_length)