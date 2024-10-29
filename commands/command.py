from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        """Executa a ação."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Desfaz a ação."""
        pass
