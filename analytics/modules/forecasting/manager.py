from interfaces.manager import Manager
from modules.logs.loggers import GeneralLogger
from modules.forecasting.extractor import TimeForecastingExtractor
from modules.forecasting.transformer import TimeForecastingTransformer
from modules.forecasting.trainer import TimeForecastingTrainer
from modules.forecasting.loader import TimeForecastingLoader


class TimeForecastingManager(Manager):
    
    _execution_parameters = None
    
    @classmethod
    def perform_process(cls, execution_parameters: dict) -> dict:
        """Perform process methods take the function to be executen from a dictionaty,
            check if is implemented in the class, and then run it

        :param execution_parameters: dictionary that containg the fucntion to be executed and
        the execution parameters
        :type execution_parameters: dict
        :return: dictionary with the execution results
        :rtype: dict
        """
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

        params = {
            "remote_path": "testing_folder/test_file.csv",
            "data": model_data
        }
        TimeForecastingLoader.save_data_in_firebase_bucket_from("dataframe",**params)
        
        
        result = {
            "success": True,
            "model_path": params.get("remote_path")
        }
        return result
        