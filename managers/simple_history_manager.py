from abstracts.history_handler_abstract import AbstractHistoryHandler
from commands.command import Command
from typing import List

class SimpleHistoryHandler(AbstractHistoryHandler):
    def __init__(self) -> None:
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []

    def push(self, command: Command) -> None:
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self) -> bool:
        if not self.can_undo():
            print("SimpleHistoryHandler: Nenhuma ação para desfazer.")
            return False
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        print(f"SimpleHistoryHandler: Comando {command.__class__.__name__} desfeito.")
        return True

    def redo(self) -> bool:
        if not self.can_redo():
            print("SimpleHistoryHandler: Nenhuma ação para refazer.")
            return False
        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)
        print(f"SimpleHistoryHandler: Comando {command.__class__.__name__} refeito.")
        return True

    def can_undo(self) -> bool:
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0
