from fastapi import APIRouter
from analytics.modules.analytic_extractor import AnalyticExtractor
from modules.apirest_endpoints import AnalyticEndPoints
from utils.utility_functions import create_folder_if_not_exist, read_json_file_from
from pandas import DataFrame, read_csv
from pathlib import Path
import configs


class ApiRestManager:
    _router = None

    @classmethod
    def setup(cls) -> None:
        print(":::..::: Starting Setup for APIREST of Analytic component :::..:::")
        cls._setup_router()

    @classmethod
    def _setup_router(cls) -> None:
        print("* Adding all endpoints to 'router' attribute")
        cls._router = APIRouter()
        cls._router.add_api_route(**AnalyticEndPoints.get_index_endpoint())
        cls._router.add_api_route(**AnalyticEndPoints.get_forecasting_endpoint())
        cls._router.add_api_route(**AnalyticEndPoints.get_test_endpoint())
        print("Done..")

    @classmethod
    def get_router(cls):
        return cls._router
