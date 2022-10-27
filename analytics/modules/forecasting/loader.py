from modules.logs.loggers import GeneralLogger
from modules.repository.firebase_client import FireBaseClient
from io import StringIO


class TimeForecastingLoader:
  
    @classmethod
    def save_data_in_firebase_bucket_from(cls, key:str, **kwargs):
        """ Method to save data in a firebase bucket
        Allow to save data using both, a local file path and a StringIo obcjet

        :param key: file_name or data frame
        :type key: str
        """
        
        firebase_manager = FireBaseClient("interperia-test")
        GeneralLogger.put_log("* Loading data in firebase storage service")
        
        if key=="local_path":
            local_path = kwargs.get("local_path")
            remote_path = kwargs.get("remote_path")
            result = firebase_manager.save_in_bucket(local_path, remote_path)
            
        elif key == "dataframe":
            buffer = StringIO()
            kwargs.get("data").to_csv(buffer, index=False)
            remote_path = kwargs.get("remote_path")
            result = firebase_manager.save_in_bucket(buffer.getvalue(), remote_path)
            
        else:
            GeneralLogger.put_log("load method not alloweds")
        
        if result == "success":
            GeneralLogger.put_log(f"* Data successfully saved in: {remote_path}")
        else:
            GeneralLogger.put_log(f"* Error: Exception happened: {result}")
        
