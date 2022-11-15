from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from pandas import DataFrame
from modules.logs.loggers import GeneralLogger
from numpy import reshape, array
from sklearn.preprocessing import MinMaxScaler


class ForecastingTrainer:
    _model = None
    _scaler = None

    @classmethod
    def setup_lstm_neuronal_network(
        cls,
        units: int,
        look_back: int,
        activation: str = "relu",
        loss: str = "mean_squared_error",
        metrics: list = ["mse", "mae"],
    ):
        cls._model = Sequential()
        cls._model.add(LSTM(units, input_shape=(1, look_back), activation=activation))
        cls._model.add(Dense(1))
        cls._model.compile(loss=loss, optimizer="adam", metrics=metrics)

    @classmethod
    def preprocessing(cls, data: DataFrame,look_back: int, training_len: float) -> dict:
        """Function used to preprocess the raw data. return a dataset for training and
        another for testing
        :param data: dataframe with the data
        :type data: DataFrame
        :param look_back: _description_
        :type look_back: int
        :param training_len: fraction of the data to be used on the training stage
        :type training_len: float
        :return: dictionary with the preprocessed data (training and test) in the
        following format:
                        {
                            "training_dataset": [train_data_in_x-axis, train_data_in_y-axis],
                            "test_dataset": [test_data_in_x-axis, test_data_in_y-axis]
                        }
        :rtype: dict
        """
        # convert daframe in a numpy array
        df = data.values.astype("float32")

        # normalize the dataset
        cls._scaler = MinMaxScaler(feature_range=(0, 1))
        df = cls._scaler.fit_transform(df)

        # split into train and test sets
        train_size = int(len(data) * training_len)
        train, test = df[0:train_size, :], df[train_size : len(df), :]

        # reshape into X=t and Y=t+1
        trainX, trainY = cls._convert_to_matrix(train, look_back)
        testX, testY = cls._convert_to_matrix(test, look_back)

        # reshape input to be [samples, time steps, features]
        trainX = reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        return {"training_dataset": [trainX, trainY], "test_dataset": [testX, testY]}

    @classmethod
    def fit_model(cls, data: dict, epochs: int, batch_size: int, verbose=False) -> dict:
        """_summary_

        :param model: _description_
        :type model: Sequential
        :param data: _description_
        :type data: dict
        :param epochs: _description_, defaults to 100
        :type epochs: int, optional
        :return: _description_
        :rtype: _type_
        """
        try:
            history = cls._model.fit(
                data.get("training_data")[0],
                data.get("training_data")[1],
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(data.get("test_data")[0], data.get("test_data")[1]),
                callbacks=[EarlyStopping(monitor="val_loss", patience=10)],
                verbose=verbose,
                shuffle=False,
            )

            train_predict = cls._model.predict(data.get("training_data")[0])
            test_predict = cls._model.predict(data.get("test_data")[0])

            result = {
                "result": "success",
                "history": history,
                "training_predict": train_predict,
                "test_predict": test_predict,
            }
            return result

        except Exception as e:
            return {"result": "fail", "message": e}


    @classmethod
    def plot_result(cls):
        pass

    @staticmethod
    def _convert_to_matrix(dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return array(dataX), array(dataY)
