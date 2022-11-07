from pandas import DataFrame
from modules.logs.loggers import GeneralLogger
from numpy import reshape, array
from sklearn.preprocessing import MinMaxScaler


class ForecastingTransformer:

    @classmethod
    def preprocessing(cls, data: DataFrame, look_back: int, training_len: float) -> dict:
        """Function used to preprocess the raw data. return a dataset for training and
        another for testing
        :param data: dataframe with the data
        :type data: DataFrame
        :param look_back: _description_
        :type look_back: int
        :param training_len: fraction of the data to be used on the training stage
        :type training_len: float
        :return: dictionary with the preprocessed data (training and test)
        :rtype: dict
        """
        train_size = int(len(data) * training_len)
        df = data.values.astype("float32")
        scaler = MinMaxScaler(feature_range=(0, 1))
        df = scaler.fit_transform(reshape(df, (-1, 1)))

        trainX, trainY = cls._convert_to_matrix(df[0:train_size, :], look_back)
        testX, testY = cls._convert_to_matrix(df[train_size : len(df), :], look_back)
        
        trainX = reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = reshape(testX, (testX.shape[0], 1, testX.shape[1]))
        return {"training_data": [trainX, trainY], "test_data": [testX, testY]}
    
    
    @staticmethod
    def _convert_to_matrix(data: array, look_back: int):
        X, Y = [], []
        for i in range(len(data) - look_back):
            d = i + look_back
            X.append(data[i:d,])
            Y.append( data[d,])
            return array(X), array(Y)
