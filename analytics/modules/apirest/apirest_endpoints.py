from utils.utility_functions import json_message
from fastapi import Request
from modules.logs.loggers import GeneralLogger
from modules.forecasting.manager import TimeForecastingManager

class AnalyticEndPoints:
    @classmethod
    async def _index_endpoint(cls):
        GeneralLogger.put_log("APIREST is working...")
        return json_message("APIREST is working...")

    @classmethod
    async def _forecasting_endpoint(cls, request: Request) -> dict:
        """
        This method is used to build a predictive model with historical data from a single cluster
        The data will be sent in a post request with the following format:
        :param request: data in json format sent in a post request
        :return: dictionary with the path in a AWS/Firebase bucket containing the files with the predictive model
        
        Example: 
            {
                data: [
                        {date: str (dd/mm/yyyy), counts: array},
                        {date: str (dd/mm/yyyy), counts: array},
                        {date: str (dd/mm/yyyy), counts: array},
                                    .
                                    .
                                    .
                        {date: str (dd/mm/yyyy), counts: array},
                ]
            }

        Counts is an array of length 24, and represents the number of incidents in a one hour interval.
        For example, the first position represent the counts for the interval 00:00 to 00:59, second position
        represent the counts for the interval from 01:00 to 01:59 and continues with the same logic up to 23:59
        """
 
        execution_parameters = {
            "process_function": "build_predictive_model",
            "json_content": await request.json()
        }
        
        result = TimeForecastingManager.perform_process(execution_parameters)
        return result

    @classmethod
    async def _test_endpoint(cls, request: Request):
        message = {
            "message": "Testing apirest",
            "host": request.client.host,
            "method": request.method,
        } 
        return message

    @classmethod
    async def _forecasting_test_endpoint(cls, request: Request) -> dict:
        """
        This method will be used to test predictive models by obtaining data directly from the database. Thus,
        the data will not be obtained from a post-type request, but from a connection to the databases.
        :param request: json with information about what database will be used and which cluster
        :type request: Request
        :return: _description_
        :rtype: dict
        """
        # TODO: use etl method to get data from mysql database (try to get data by day and group bu hour)
        # TODO: Build a class to create the predictive models
        pass

    # ::::::......:::::: Getter Methods ::::::......::::::
    @classmethod
    def get_index_endpoint(cls):
        params = {
            "path": "/", 
            "endpoint": cls._index_endpoint,
            "methods": ["GET"]}
        return params

    @classmethod
    def get_forecasting_endpoint(cls):
        params = {
            "path": "/forecasting",
            "endpoint": cls._forecasting_endpoint,
            "methods": ["POST"],
        }
        return params

    @classmethod
    def get_test_endpoint(cls):
        params = {
            "path": "/test_endpoint",
            "endpoint": cls._test_endpoint,
            "methods": ["GET"],
        }
        return params
