from utils.utility_functions import json_message
from fastapi import Request
from utils.models import Location


class AnalyticEndPoints:

    @classmethod
    async def _index_endpoint(cls):
        return json_message("APIREST is working...")

    @classmethod
    async def _forecasting_endpoint(cls, location: Location):
        return json_message("This is not ready yet.")

    @classmethod
    async def _test_endpoint(cls, request: Request):
        message = {
            "message": "Testing apirest",
            "host": request.client.host,
            "method": request.method
        }
        return message

    @classmethod
    def get_index_endpoint(cls):
        params = {
            "path": "/",
            "endpoint": cls._index_endpoint,
            "methods": ["GET"]
        }
        return params

    @classmethod
    def get_forecasting_endpoint(cls):
        params = {
            "path": "/forecasting",
            "endpoint": cls._forecasting_endpoint,
            "methods": ["POST"]
        }
        return params

    @classmethod
    def get_test_endpoint(cls):
        params = {
            "path": "/test_endpoint",
            "endpoint": cls._test_endpoint,
            "methods": ["GET"]
        }
        return params
