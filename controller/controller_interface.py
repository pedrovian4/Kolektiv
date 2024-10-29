from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def show(self) -> None:
        pass

