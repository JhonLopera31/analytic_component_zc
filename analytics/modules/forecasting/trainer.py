from pandas import DataFrame
from modules.logs.loggers import GeneralLogger
from numpy import array


class ForecastingTrainer:

    @classmethod
    def DummyTraining(cls, data: DataFrame) -> DataFrame:
        GeneralLogger.put_log("Dummy training")
        return data
    
        
    @classmethod
    def preprocessing(data: DataFrame):
        pass
    
    @classmethod
    def setup_neuronal_network(cls):
        pass
    
    @classmethod
    def fit_model(cls):
        pass
    
    
    @staticmethod
    def convert_to_matrix(data: array, look_back: int):
        X, Y = [], []
        for i in range(len(data)-look_back):
            d=i+look_back  
            X.append(data[i:d,])
            Y.append(data[d,])
            return array(X), array(Y)