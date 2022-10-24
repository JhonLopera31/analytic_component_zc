from modules.logs.loggers import GeneralLogger
from modules.repository.firebase_client import FireBaseClient
from io import StringIO


class TimeForecastingLoader:

    @classmethod
    def Load_file_in_bucket(cls, data,  remote_path: str):
        GeneralLogger.put_log("* Loading data in firebase storage service")
        firebase_manager = FireBaseClient("interperia-test")
        result = firebase_manager.save_in_bucket(StringIO(data), remote_path)
        
        if result == "success":
            GeneralLogger.put_log(f"* Data successfully saved in: {remote_path}")
        else:
            GeneralLogger.put_log(f"* Error: Exception happened: {result}")
        
