import pandas as pd
import numpy as np
from gamspy import SpecialValues

# This class is used to deal with parameters in the model
class GSA_parameters :
    def __init__(self, input_file):
        self.input = pd.read_csv(input_file)
        self.parameters = self.input["Parameter"]

    def load_sets(self):
        sets = "FUELPRICE, SOSIBU2INDIC, SOSIBUBOUND"
        return sets
    
    def update_input(self, scenario_data, sample):
        
        #Fossil fuel price

        FUELPRICE = scenario_data["FUELPRICE"]
        FUELPRICE.columns = ["YYY", "AAA", "FFF", "value"]
        FUELPRICE.loc[(FUELPRICE["FFF"]=="NATGAS") & (FUELPRICE["value"]>=1e-320),"value"]*=sample["FOSSIL_P"]

        SOSIBU2INDIC = scenario_data["SOSIBU2INDIC"]
        SOSIBU2INDIC.columns = ["YYY", "PROC", "FLOW", "FLOWINDIC", "value"]
        SOSIBU2INDIC.loc[(SOSIBU2INDIC["FLOWINDIC"]=="OPERATIONCOST") 
                       & (SOSIBU2INDIC["FLOW"].isin(["DIESELFLOW","KEROSENEFLOW","LNGFLOW","MDOFLOW"])) 
                       & (SOSIBU2INDIC["value"]>=1e-320),"value"]*= sample["FOSSIL_P"]

        #Renewable fuel import price

        SOSIBU2INDIC.loc[(SOSIBU2INDIC["FLOW"].isin(["AMMONIA_IMPORT","HYDROGEN_IMPORT","FT_IMPORT","METHANOL_IMPORT"])) 
                       & (SOSIBU2INDIC["value"]>=1e-320),"value"]*=sample["FUEL_IMPORT_P"]

        #Renewable fuel import availability

        SOSIBUBOUND = scenario_data["SOSIBUBOUND"]
        SOSIBUBOUND.columns = ["YYY", "AAA", "PROC", "FLOW", "ILOUPFXSET", "value"]
        SOSIBUBOUND.loc[(SOSIBUBOUND["ILOUPFXSET"]=="ILOUPFX_UP") 
                      & (SOSIBUBOUND["FLOW"].isin(["AMMONIA_IMPORT","HYDROGEN_IMPORT","FT_IMPORT","METHANOL_IMPORT"])) 
                      & (SOSIBUBOUND["value"]>=1e-320),"value"]*= sample["FUEL_IMPORT_LIM"]

        return scenario_data