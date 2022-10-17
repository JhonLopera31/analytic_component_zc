from abc import ABC, abstractmethod


class Manager(ABC):
    @classmethod
    @abstractmethod
    def perform_process(cls, process_function: str):
        pass
