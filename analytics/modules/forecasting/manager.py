from interfaces.manager import Manager
from modules.logs.loggers import GeneralLogger
from modules.forecasting.extractor import ForecastingExtractor
from modules.forecasting.transformer import ForecastingTransformer
from modules.forecasting.trainer import ForecastingTrainer
from modules.forecasting.loader import ForecastingLoader


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
        assert hasattr(cls, process_function), "Process not defined"

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
        try:
            look_back = 30
            GeneralLogger.put_log("* Setting neuronal network")
            ForecastingTrainer.setup_neuronal_network(look_back=look_back)
            
            GeneralLogger.put_log("* Performing data extraction process")
            json_content = cls._execution_parameters.get("json_content")
            training_data = ForecastingExtractor.extract_training_data(json_content)

            GeneralLogger.put_log("* Performing data transformation process")
            training_data = ForecastingTransformer.preprocessing(training_data, 30, 0.8)

            GeneralLogger.put_log("* Performing training process")
            trainig_result = ForecastingTrainer.fit_model(training_data,epochs=100)


            #::::::......::: Load data in Firebase bucket :::......::::::
            GeneralLogger.put_log("* Performing loading process")
            
            params = {
                "firebase_folder": "forecasting_models",
                "file_name": f"{json_content.get('id')}_training_model.csv",
                "data": trainig_result,
            }
            result = ForecastingLoader.save_data_in_bucket("dataframe", params)

            return result

        except Exception as e:
            return e
