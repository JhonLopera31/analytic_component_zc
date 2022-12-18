from interfaces.manager import Manager
from modules.logs.loggers import GeneralLogger
from modules.forecasting.extractor import ForecastingExtractor
from modules.forecasting.trainer import ForecastingTrainer
from modules.forecasting.loader import ForecastingLoader
from pandas import read_csv
from numpy import arange
import matplotlib.pyplot as plt
from numpy import arange
import tensorflow as tf


class TimeForecastingManager(Manager):

    _execution_parameters = None

    @classmethod
    def perform_process(cls, execution_parameters: dict) -> dict:
        """Perform process methods takes the name of the function to be executen from a dictionaty,
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
        
        look_back = 7
        units = 100
        training_size = 0.7
        epochs = 100
        batch_size = 4
        
        GeneralLogger.put_log("* Setting neuronal network")
        ForecastingTrainer.setup_lstm_neuronal_network(units, look_back)
        
        GeneralLogger.put_log("* Performing Data extraction")
        json_content = cls._execution_parameters.get("json_content")
        data = ForecastingExtractor.extract_training_data(json_content)
        data = read_csv('/Users/andersonlopera/Desktop/LSTM/airline-passengers.csv', usecols=[1], engine='python')

        GeneralLogger.put_log("* Preprocesing data")
        training_data = ForecastingTrainer.preprocessing(data, look_back, training_size)
        
        GeneralLogger.put_log("* Performing training process")
        trainig_result = ForecastingTrainer.fit_model(training_data, epochs, batch_size)
        
        dataset = data.values
        dataset = dataset.astype('float32')
        train_size = int(len(dataset) * 0.7)
        train_plot, test_plot = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

        x = arange(0, len(train_plot),1)
        plt.plot (trainig_result.get("train_predict"),"o--", label = "prediction")
        plt.plot(x-(look_back-1),train_plot,"x--", label = "original")
        plt.legend()
        plt.show()

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
    def search_grid(cls, data):
        
        training_size = 0.8
        epochs = 100
        batch_size_array = [32,64]
        look_back_array = arange(7, 60, 7)
        units_array = arange(10,100, 10)
        
        for look_back in look_back_array:
            for units in units_array:
                for batch_size in batch_size_array:
                    GeneralLogger.put_log("* Preprocesing data")
                    training_data = ForecastingTrainer.preprocessing(data, look_back, training_size)
        
                    GeneralLogger.put_log("* Setting neuronal network")
                    ForecastingTrainer.setup_lstm_neuronal_network(units, look_back)

                    GeneralLogger.put_log("* Performing training process")
                    trainig_result = ForecastingTrainer.fit_model(training_data, epochs, batch_size)

