from interfaces.manager import Manager
from modules.logs.loggers import GeneralLogger
from modules.forecasting.extractor import ForecastingExtractor
from modules.forecasting.trainer import ForecastingTrainer
from modules.forecasting.loader import ForecastingLoader
from pandas import read_csv, DataFrame
from numpy import arange

import tensorflow as tf


class TimeForecastingManager(Manager):

    _execution_parameters = None

    @classmethod
    def perform_process(cls, execution_parameters: dict) -> dict:
        """
        Perform process methods takes the name of the function to be executen from a dictionaty,
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
        :rtype: dictx
        """

        tf.random.set_seed(7)
        
        GeneralLogger.put_log("* Performing Data extraction")
        json_content = cls._execution_parameters.get("json_content")
        data = ForecastingExtractor.extract_training_data(json_content)
        data = read_csv("/Users/andersonlopera/Desktop/LSTM/airline-passengers.csv",usecols=[1],engine="python")
        
        best_parameters = cls.search_grid(data=data)

        look_back = best_parameters.get("look_back")
        units = best_parameters.get("units")
        batch_size = best_parameters.get("batch_size")
        training_size = best_parameters.get("training_size")
        epochs = 100
        
        
        GeneralLogger.put_log("* Setting neuronal network")
        ForecastingTrainer.setup_lstm_neuronal_network(units, look_back)

        GeneralLogger.put_log("* Preprocesing data")
        training_data = ForecastingTrainer.preprocessing(data, look_back, training_size)

        GeneralLogger.put_log("* Performing training process")
        trainig_result = ForecastingTrainer.fit_model(training_data, epochs, batch_size)

        ForecastingTrainer.plot_result(data, trainig_result, look_back, training_size)

        #::::::......::: Load data in a Firebase bucket :::......::::::
        GeneralLogger.put_log("* Performing loading process")

        params = {
            "firebase_folder": "forecasting_models",
            "file_name": f"{json_content.get('id')}_training_model.csv",
            "data": trainig_result,
        }
        # result = ForecastingLoader.save_data_in_bucket("dataframe", params)

        return {"test": "test"}

    @classmethod
    def search_grid(cls, data: DataFrame) -> dict:

        training_size = 0.7
        epochs = 100
        batch_size_array = [32, 64]
        look_back_array = arange(3,22, 5)
        units_array = arange(10, 101, 10)

        GeneralLogger.put_log("Searching the best parameters ...")

        scores = []
        parameters = {}
        iteration = 0

        for look_back in look_back_array:
            for units in units_array:
                for batch_size in batch_size_array:
                    
                    GeneralLogger.put_log(f"* Setting neuronal network")
                    ForecastingTrainer.setup_lstm_neuronal_network(units, look_back)

                    GeneralLogger.put_log("* Preprocesing data")
                    training_data = ForecastingTrainer.preprocessing(data, look_back, training_size)

                    GeneralLogger.put_log("* Performing training process")
                    results = ForecastingTrainer.fit_model(training_data, epochs, batch_size)
                    
                    scores.append(results.get("rmse").get("training_score"))
                    parameters[iteration] = {
                        "look_back": look_back,
                        "units": units,
                        "batch_size": batch_size,
                        "training_size": training_size
                    }
                    GeneralLogger.put_log(f"i: {iteration}, parameters: {parameters.get(iteration)}")
                    GeneralLogger.put_log(f"MSE: {results.get('mse')}")
                    iteration += 1
                   
        best_parameters = parameters.get(scores.index(min(scores)))
        GeneralLogger.put_log(f"Best parameters {best_parameters}")
        
        return best_parameters
        