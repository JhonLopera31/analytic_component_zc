from interfaces.manager import Manager
from modules.logs.loggers import GeneralLogger
from modules.forecasting.extractor import TimeForecastingExtractor


class TimeForecastingManager(Manager):
    
    _execution_parameters = None
    
    @classmethod
    def perform_process(cls, execution_parameters: dict):   
        cls._execution_parameters = execution_parameters
        process_function = execution_parameters.get("process_function")
        assert hasattr(cls,process_function), "you mus provide a correct process function"
        GeneralLogger.put_log(f"::::.....:::: Time Forecasting ::::.....::::")
        return getattr(cls, process_function)()


    @classmethod
    def build_predictive_model(cls) -> dict:
        """This method use the data of a given cluster to build the predictive model files
        and store them in a S3/Firebase bucket
        :param json_content: data with security incident counts by hour, and grouped by day
        :type json_content: dict
        :return: Path of the bucket where the predicive model files were stored
        :rtype: str
        """
        json_content = cls._execution_parameters.get("json_content")
        training_data = TimeForecastingExtractor.extract_training_data(json_content)
        
        result = {
            "success": True,
            "model_path": "/test_folder/test_file.test"
        }
        return result
        