from modules.logs.loggers import GeneralLogger
from modules.repository.firebase_client import FireBaseClient
from io import StringIO


class ForecastingLoader:
    @classmethod
    def save_data_in_bucket(cls, method: str, params: dict):
        """Method to save data in a firebase bucket
        Allow to save data using both, a local file path and a StringIo obcjet
        :param method: if the data will be loaded from file_name or data frame
        :type key: str
        """

        firebase_manager = FireBaseClient("interperia-test")
        GeneralLogger.put_log("* Loading data in firebase storage service")

        if method == "local_path":
            local_path = params.get("local_path")
            remote_path = f"{params.get('firebase_folder')}/{params.get('file_name')}"
            result = firebase_manager.save_in_bucket(local_path, remote_path)

        elif method == "dataframe":
            buffer = StringIO()
            params.get("data").to_csv(buffer, index=False)
            remote_path = f"{params.get('firebase_folder')}/{params.get('file_name')}"
            result = firebase_manager.save_in_bucket(buffer.getvalue(), remote_path)

        else:
            GeneralLogger.put_log("Provide a valid load method")

        if result == "success":
            GeneralLogger.put_log(f"* Data successfully saved in: {remote_path}")
            return {"operation_result":result, "remote_path": remote_path}
        else:
            GeneralLogger.put_log(f"* Error: Exception happened: {result}")
            return {"operation_result":result}
