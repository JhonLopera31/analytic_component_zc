from config.settings import ANALYTIC_PROCESSOR
from modules.etls.extractors import AnalyticExtractor

class AnalyticManager:
    
    @classmethod
    def perform_process(cls, process_function: str):
        processor_exist = process_function in ANALYTIC_PROCESSOR 
        assert processor_exist, Exception('You must provide a valid process function')
        getattr(cls, process_function)()
        
    
    @classmethod 
    def run_forecasting(cls):
        print("Test is working")
        