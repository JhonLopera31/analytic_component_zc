from fastapi import APIRouter
from modules.apirest.apirest_endpoints import AnalyticEndPoints
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import APIREST_CONFIGURATIONS
from modules.logs.loggers import GeneralLogger


class ApiRestManager:

    @classmethod
    def setup(cls) -> FastAPI:
        GeneralLogger.put_log("::::.... Starting APIREST setup (Analytic component) .....::::")
        app = FastAPI()
        app.include_router(cls._setup_router())  
        app.add_middleware(CORSMiddleware,**APIREST_CONFIGURATIONS)
        return app
        
             
    @classmethod
    def _setup_router(cls) -> APIRouter:
        GeneralLogger.put_log("* Adding all endpoints to a router class")
        router = APIRouter()
        router.add_api_route(**AnalyticEndPoints.get_index_endpoint())
        router.add_api_route(**AnalyticEndPoints.get_forecasting_endpoint())
        router.add_api_route(**AnalyticEndPoints.get_test_endpoint())
        return router
