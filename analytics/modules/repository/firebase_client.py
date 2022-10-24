from pyrebase import initialize_app
from os import getenv
from config.settings import FIREBASE_CONFIG


class FireBaseClient:
    
    
    def __init__(self, project_name: str) -> None:
        
        self._firebase_client = initialize_app(self._get_config(project_name))
        
    
    def _get_config(self, project_name:str):
        
        credentials_name = FIREBASE_CONFIG.get(project_name).get(["credentials_name"])
        credentials = getenv(credentials_name).split(",")
        
        firebase_config = {
            "apiKey": credentials[0],
            "authDomain": credentials[1],
            "projectId": credentials[2],
            "storageBucket": credentials[3],
            }
        
        return firebase_config
        
        
    def save_in_bucket(self, local_path: str,  remote_path:str):
        storage_client = self._firebase_client.storage()
        try:
            storage_client.child(remote_path).put(local_path)
            return "success"
        except Exception as e:
            print(f"something goes wrong {e}")
            return e
            
            
    def download_from_bucket(self, local_path: str,  remote_path:str):
        storage_client = self._firebase_client.storage()
        try:
            storage_client.child(remote_path).download(local_path)
            return True
        except Exception as e:
            print(f"something goes wrong {e}")   
            return False