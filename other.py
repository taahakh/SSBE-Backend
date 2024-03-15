import importlib
import json

from model_interface import SummaryType

class SummarisationManager:

    def __init__(self):
        self.model_list = {}
        self.curr_loaded_model = None;
        self.load_resources()
        self.create_model_descriptors()

    def create_model_descriptors(self):
        
        descriptor_list = []

        for _, value in self.model_list.items():
            if value.summary_type.value == "Abstractive": 
                st = "ab" 
            else :
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

            print(value.summary_type.value)
        
            descriptor_list.append(model_descriptor)
        
        with open('md.json', 'w') as file:
            json.dump(descriptor_list, file, indent=2)


    def load_resources(self):

        with open('model_list.txt', 'r') as file:
            model_list = file.read().splitlines()
            print(model_list)

        for model in model_list:
            model = importlib.import_module("models."+model)
            self.model_list[model.Model().model_name] = model.Model()
        
        print(self.model_list)

    def model_loader(self, model):
        print(model)
        if self.curr_loaded_model is not None:
            self.curr_loaded_model.unload_model()
        print("ok")
        m = self.model_list[model]
        print(m)
        m.load_model()
        self.curr_loaded_model = m
        return m
    
    def is_model_abstractive(self, model_name):
        return self.model_list[model_name].summary_type == SummaryType.ABSTRACTIVE
        
    def summarise(self, text, model_name, summary_length):
        # model = self.model_list[model_name]
        # model.load_model()
        print("Loading Model...")
        # print
        model = self.model_loader(model_name)
        print("Model Loaded")
        print("Summarising...")
        state, output = model.summarise(text, summary_length)
        print('STATE: ' + str(state))
        if state:
            return output
        return "FAILED"   