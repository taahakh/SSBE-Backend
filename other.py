import importlib
import json
#Uncomment
# import models.bartlargecnn

# , models.bartxiv, models.t5medical


# m = models.bartxiv.BartXIV()

# Uncomment
# m = models.bartlargecnn.BartLargeCNN()

# Uncomment
# def summarise(text):
#     m.load_model()
#     state, output = m.summarise(text);
#     print('STATE: ' + str(state))
#     if state:
#         return output
#     return "FAILED"

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
        
    def summarise(self, text, model_name):
        # model = self.model_list[model_name]
        # model.load_model()
        print("Loading Model...")
        # print
        model = self.model_loader(model_name)
        print("Model Loaded")
        print("Summarising...")
        state, output = model.summarise(text)
        print('STATE: ' + str(state))
        if state:
            return output
        return "FAILED"   
        


# sm = SummarisationManager();
# sm.model_loader('BartLargeCNN')

# sm.load_resources();



# from transformers import pipeline

# pipe = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

# def summarise(text):
#     return pipe(text, min_length=100, max_length=500)[0]['summary_text']



# def summarise(text):
#     inputs = tokenizer(text, return_tensors="pt")
#     outputs = model.generate(inputs["input_ids"], num_beams=4, min_length=100, max_length=500)
#     return tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]






# inputs = tokenizer(input_text, return_tensors="pt")
# outputs = model(**inputs)

# summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=100, max_length=500)
# print(tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])