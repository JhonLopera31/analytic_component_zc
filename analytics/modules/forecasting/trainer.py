from modules.logs.loggers import GeneralLogger
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt


class ForecastingTrainer:
    _model = None


    @classmethod
    def setup_neuronal_network(cls, look_back: int) -> None:
        cls._model  = Sequential()
        cls._model.add(LSTM(100, input_shape=(1, look_back), activation="relu"))
        cls._model.add(Dense(1))
        cls._model.compile(loss="mean_squared_error",optimizer="adam",metrics=["mse", "mae"])


    @classmethod
    def fit_model(cls, data:dict, epochs=100) -> dict:
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
                batch_size=30,
                validation_data=(data.get("test_data")[0],data.get("test_data")[1]),
                callbacks=[EarlyStopping(monitor="val_loss", patience=10)],
                verbose=1,
                shuffle=False,
            )
            
            train_predict = data.get("training_data")[0]
            test_predict = data.get("test_data")[0]
            result = {
                "result": "success",
                "history": history,
                "training_predict": train_predict,
                "test_predict": test_predict
            }
            return result
        
        except Exception as e:
            return {"result":"fail", "message": e}
    
    
    @classmethod
    def get_model(cls):
        return cls._model
    
            
    @staticmethod
    def plot_model_loss(history):
        plt.figure(figsize=(8,4))
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Test Loss')
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epochs')
        plt.legend(loc='upper right')
        plt.show()
