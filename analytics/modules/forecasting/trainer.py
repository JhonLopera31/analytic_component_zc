from pandas import DataFrame
from modules.logs.loggers import GeneralLogger

class TimeForecastingTrainer:

    @classmethod
    def DummyTraining(cls, data: DataFrame) -> DataFrame:
        GeneralLogger.put_log("Dummy training")
        return data