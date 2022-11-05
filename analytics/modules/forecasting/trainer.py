from pandas import DataFrame
from modules.logs.loggers import GeneralLogger

class ForecastingTrainer:

    @classmethod
    def DummyTraining(cls, data: DataFrame) -> DataFrame:
        GeneralLogger.put_log("Dummy training")
        return data