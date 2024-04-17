import os

# Installing the required packages
os.system("pip install -r requirements.txt")

# Installing the models
import summarisationmanager

s = summarisationmanager.SummarisationManager()

# Loading the models will install the models
for model in s.model_list:
    s.model_list[model].load_model()
    s.model_list[model].unload_model()