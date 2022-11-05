from pandas import DataFrame
from modules.logs.loggers import GeneralLogger

class ForecastingTransformer:

    @classmethod
    def DummyTransformation(cls,data: DataFrame) -> DataFrame:
        GeneralLogger.put_log("Dummy transformation")
        return data
