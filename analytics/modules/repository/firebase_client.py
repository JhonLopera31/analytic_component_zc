from firebase_admin import initialize_app, storage
from firebase_admin import credentials
from os import getenv
from config.settings import FIREBASE_CONFIGS


class FireBaseClient:
    def __init__(self, project_name: str) -> None:
        cred, bucket = self._get_configs(project_name)
        self._firebase_client = initialize_app(cred, bucket)

    def _get_configs(self, project_name: str):
        """This function is used get the Firebase credentials and the bucket from project settings
           Credentials will obtained from a json file generated for the service acount of the project 
           in firebase. This credentials must no be shared in a public repository
        :param project_name: name of the project in variable FIREBASE_CONFIGS in the file settings.py
        :type project_name: Creadentials object and bucket name
        :return: _description_
        :rtype: credeantialsObject, str
        """
        service_account_keys = FIREBASE_CONFIGS.get(project_name).get("keys_path")
        cred = credentials.Certificate(service_account_keys)
        bucket = {
            "storageBucket": FIREBASE_CONFIGS.get(project_name).get("bucket_name")
        }
        return cred, bucket

    def save_in_bucket(self, local_path: str, remote_path: str):
        """Save method can be use to load files in the firebase bucket.
        This method allows to load files saved locally, using the path, or ussing a 
        buffer created with a StringIO object

        :param local_path: path or StringIO object of the data to save in bucet
        :type local_path: str or StringIO
        :param remote_path: Path in the Firebase bucket where the file will be saved
        :type remote_path: str
        :return: success message or exception message
        :rtype: str or Exception
        """
        try:
            bucket = storage.bucket()
            blob = bucket.blob(remote_path)
            blob.upload_from_string(local_path)
            return "success"

        except Exception as e:
            return e

    def download_file(self, remote_path: str, local_path: str):
        """Function used to download a file from a firebase bucket

        :param remote_path: Path in the Firebase bucket where the file is saved
        :type remote_path: str
        :param local_path: Path where the file will be saved
        :type local_path: str
        :return: success message or exception message
        :rtype: str or Exception
        """
        try:
            bucket = storage.bucket()
            blob = bucket.blob(remote_path)
            blob.download_to_filename(local_path)
            return "success"
        except Exception as e:
            return e
