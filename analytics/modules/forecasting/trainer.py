from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from pandas import DataFrame
from numpy import reshape, array
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from numpy import sqrt


class ForecastingTrainer:
    _model = None
    _scaler = None

    @classmethod
    def setup_lstm_neuronal_network(
        cls,
        units: int,
        look_back: int,
        activation: str = "relu",
        loss: str = "mean_squared_error", #mae
        metrics: list = ["mse", "mae"], #Use r2_score from keras as well https://stackoverflow.com/questions/45250100/kerasregressor-coefficient-of-determination-r2-score
    ):
        cls._model = Sequential()
        cls._model.add(LSTM(units, input_shape=(1, look_back), activation=activation))
        cls._model.add(Dense(1))
        cls._model.compile(loss=loss, optimizer="adam", metrics=metrics)
        
        # TODO: Parameters to optimize: unit and look_back
        
        #unit, look_back (Tomar un tiempo que pueda coincidir con la sesionalidad de la serie),
        

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
                            "training_dataset": {"x": train_data_in_x-axis, "y": train_data_in_y-axis},
                            "test_dataset": {"x": test_data_in_x-axis, "y":test_data_in_y-axis}
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
        train_x, train_y = cls._convert_to_matrix(train, look_back)
        test_x, test_y = cls._convert_to_matrix(test, look_back)

        # reshape input to be [samples, time steps, features]
        train_x = reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
        test_x = reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))

        return {
            "training_dataset": {"x":train_x, "y":train_y}, 
            "test_dataset": {"x":test_x, "y":test_y}
        }

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
        # try:
        history = cls._model.fit(
            data.get("training_dataset").get("x"),
            data.get("training_dataset").get("y"),
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(data.get("test_dataset").get("x"), data.get("test_dataset").get("y")),
            callbacks=[EarlyStopping(monitor="val_loss", patience=10)],
            verbose=0,
            shuffle=False,
        )

        train_predict = cls._model.predict(data.get("training_dataset").get("x"))
        train_predict = cls._scaler.inverse_transform(train_predict)
        
        test_predict = cls._model.predict(data.get("test_dataset").get("x"))
        test_predict = cls._scaler.inverse_transform(test_predict)
        
        
        result = {
            "result": "success",
            "history": history,
            "rmse": cls._get_rsme(data),
            "train_predict": train_predict,
            "test_predict": test_predict
        }
        return result

        # except Exception as e:
        #     return {"result": "fail", "message": e}




    @classmethod
    def _get_rsme(cls, data) -> dict:

        train_predict = cls._model.predict(data.get("training_dataset").get("x"))
        print(type(train_predict))
        test_predict = cls._model.predict(data.get("test_dataset").get("x"))

        # invert predictions
        train_predict = cls._scaler.inverse_transform(train_predict)
        train_y = cls._scaler.inverse_transform([data.get("training_dataset").get("y")])
        test_predict = cls._scaler.inverse_transform(test_predict)
        test_y = cls._scaler.inverse_transform([data.get("test_dataset").get("y")])
        
        scores = {
            "train_score": sqrt(mean_squared_error(train_y[0], train_predict[:,0])),
            "test_score": sqrt(mean_squared_error(test_y[0], test_predict[:,0]))
        }
        print(scores) 
        
        return {
            "train_score": sqrt(mean_squared_error(train_y[0], train_predict[:,0])),
            "test_score": sqrt(mean_squared_error(test_y[0], test_predict[:,0]))
        }
        
    @classmethod
    def plot_result(cls):
        pass

    @staticmethod
    def _convert_to_matrix(dataset, look_back=1):
        data_x, data_y = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            data_x.append(a)
            data_y.append(dataset[i + look_back, 0])
        return array(data_x), array(data_y)
