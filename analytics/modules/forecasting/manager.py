from interfaces.manager import Manager
from modules.logs.loggers import GeneralLogger
from modules.forecasting.extractor import TimeForecastingExtractor
from modules.forecasting.transformer import TimeForecastingTransformer
from modules.forecasting.trainer import TimeForecastingTrainer
from modules.forecasting.loader import TimeForecastingLoader
from config.settings import FIREBASE_FORECASTING_FOLDER


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
        """
        This method use the data of a given cluster to build the predictive model files
        and store them in a S3/Firebase bucket
        :param json_content: data with security incident counts by hour, and grouped by day
        :type json_content: dict
        :return: Path of the bucket where the predictive model files were stored
        :rtype: str
        """
        GeneralLogger.put_log("* Performing data extraction process")
        json_content = cls._execution_parameters.get("json_content")
        training_data = TimeForecastingExtractor.extract_training_data(json_content)
        
        
        GeneralLogger.put_log("* Performing data transformation process")
        training_data = TimeForecastingTransformer.DummyTransformation(training_data)
        
        GeneralLogger.put_log("* Performing training process")
        model_data = TimeForecastingTrainer.DummyTraining(training_data)
        
        #::::::...... Load data in Firebase bucket ......::::::
        GeneralLogger.put_log("* Performing loading process")
        remote_path = f"{FIREBASE_FORECASTING_FOLDER}/test_cluster_name.csv"
        TimeForecastingLoader.Load_file_in_bucket(model_data, remote_path=remote_path)
        
        result = {
            "success": True,
            "model_path": remote_path
        }
        return result
        