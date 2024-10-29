from abc import ABC, abstractmethod
from commands.command import Command

class AbstractHistoryHandler(ABC):
    @abstractmethod
    def push(self, command: Command) -> None:
        """Adiciona um comando ao histórico."""
        pass

    @abstractmethod
    def undo(self) -> bool:
        """Desfaz a última ação. Retorna True se bem-sucedido, False caso contrário."""
        pass

    @abstractmethod
    def redo(self) -> bool:
        """Refaz a última ação desfeita. Retorna True se bem-sucedido, False caso contrário."""
        pass

    @abstractmethod
    def can_undo(self) -> bool:
        """Verifica se há ações para desfazer."""
        pass

    @abstractmethod
    def can_redo(self) -> bool:
        """Verifica se há ações para refazer."""
        pass
