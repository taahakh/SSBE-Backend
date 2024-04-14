import importlib
import json
import os

from model_interface import SummaryType

class SummarisationManager:

    def __init__(self, model_src_path='model_list.txt', json_output_path='md.json'):
        """
        Initialises a SummarisationManager object. Stores a list of models and creates a JSON file containing model descriptors.

        Args:
            model_src_path (str): The path to the model source file. Defaults to 'model_list.txt'.
            json_output_path (str): The path to the JSON output file. Defaults to 'md.json'.
        """
        self.model_list = {}
        self.curr_loaded_model = None;
        
        if (not self.load_resources(model_src_path)):
            print("Failed to load resources")
            exit(1)

        self.create_model_descriptors(json_output_path)

    def create_model_descriptors(self, output_path):
        """
        Creates model descriptors for each model, inherited with abstract base class ModelInterface, in the model list and saves them to a JSON file.

        Args:
            output_path (str): The path to the output JSON file.

        Returns:
            None
        """
        descriptor_list = []

        for _, value in self.model_list.items():
            if value.summary_type.value == "Abstractive": 
                st = "ab" 
            else:
                st = "ex"

            # Create API model descriptor
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
        """
        Loads specified models from the specified source path.

        Args:
            src_path (str): The path to the file containing the list of models.

        Returns:
            bool: True if the resources are successfully loaded, False otherwise.
        """

        # Check if the source path is valid
        if src_path is None or src_path == "":
            return False
        
        # Check if the file is empty
        if os.path.getsize(src_path) == 0:
            return False

        # Read the file and store the model names in a list
        with open(src_path, 'r') as file:
            model_list = file.read().splitlines()
            print(model_list)

        # Import the models
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
        """
        Loads the specified model and sets it as the current loaded model.

        Args:
            model (str): The name of the model to load.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the model was loaded successfully,
                   and the loaded model object if successful, or None if unsuccessful.
        """
        # Unload the current model if one is loaded
        if self.curr_loaded_model is not None:
            self.curr_loaded_model.unload_model()

        # Check if the model exists in the model list
        if model not in self.model_list:
            return False, None
        
        m = self.model_list[model]
        m.load_model()
        # Set the current loaded model
        self.curr_loaded_model = m

        return True, m
    
    def is_model_abstractive(self, model_name):
        """
        Checks if a given model is abstractive.

        Parameters:
        - model_name (str): The name of the model to check.

        Returns:
        - Model: The abstractive model if it exists, otherwise None.
        """
        if model_name not in self.model_list:
            return None
        
        return self.model_list[model_name] if self.model_list[model_name].summary_type == SummaryType.ABSTRACTIVE else None
        
    def summarise(self, text, model_name, summary_length):
        """
        Summarizes the given text using the specified model and summary length.

        Args:
            text (str): The text to be summarized.
            model_name (str): The name of the model to be used for summarization.
            summary_length (int): The desired length of the summary.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the model was found,
                   and the summarized text if the model was found, otherwise None.
        """
        print("Loading Model...")
        exist, model = self.model_loader(model_name)

        if not exist:
            print("Model not found")
            return exist, None

        print("Model Loaded")
        print("Summarising...")
        return model.summarise(text, summary_length)