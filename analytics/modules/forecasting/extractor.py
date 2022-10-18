from tkinter import N
from tkinter.messagebox import NO
from pandas import DataFrame


class TimeForecastingExtractor:
    
    _training_data: DataFrame = None
    
    @classmethod
    def extract_training_data(cls, json_content:dict) -> DataFrame:
        df = DataFrame(json_content.get("data"))
        df = df.join(DataFrame(df['counts'].tolist()).add_prefix('interval_'))
        cls._training_data = df.drop("counts", axis=1)
        return cls._training_data 
        
    