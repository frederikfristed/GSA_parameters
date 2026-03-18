import pandas as pd
import numpy as np
from gamspy import SpecialValues

# This class is used to deal with parameters in the model
class GSA_parameters :
    def __init__(self, input_file):
        self.input = pd.read_csv(input_file)
        self.parameters = self.input["Parameter"]

    def load_sets(self):
        sets = "FUELPRICE"
        return sets
    
    def update_input(self, scenario_data, sample):
        
        FUELPRICE = scenario_data["FUELPRICE"]
        FUELPRICE.columns = ["YYY", "AAA", "FFF", "value"]
        FUELPRICE.loc[(FUELPRICE["FFF"]=="NATGAS") & (FUELPRICE["value"]>=1e-320),"value"]*=sample["NATGAS_P"]
                
        return scenario_data