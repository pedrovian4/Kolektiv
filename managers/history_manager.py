from abstracts.history_handler_abstract import AbstractHistoryHandler
from PyQt5.QtWidgets import QMessageBox
from commands.command import Command
from view.components.atoms.status_bar import CustomStatusBar


class HistoryManager:
    def __init__(self, history_handler: AbstractHistoryHandler,controller) -> None:
        self.history_handler = history_handler
        self.main_controller = controller

    def execute_command(self, command: Command) -> None:
        self.history_handler.push(command)
        self.update_menu_actions()

    def undo_action(self) -> None:
        if self.history_handler.undo():
            self.get_main_window().update_layers_list()
            self.get_main_window().display_composited_image()
            self.get_status_bar().showMessage("Última ação desfeita.")
        else:
            QMessageBox.information(self.window, "Desfazer", "Não há ações para desfazer.")
        self.update_menu_actions()

    def redo_action(self) -> None:
        if self.history_handler.redo():
            self.get_main_window().update_layers_list()
            self.get_main_window().display_composited_image()
            self.get_status_bar().showMessage("Última ação refeita.")
        else:
            QMessageBox.information(self.window, "Refazer", "Não há ações para refazer.")
        self.update_menu_actions()

    def update_menu_actions(self) -> None:
        self.get_main_window().main_layout.undo_action.setEnabled(self.history_handler.can_undo())
        self.get_main_window().main_layout.redo_action.setEnabled(self.history_handler.can_redo())
    
    def get_main_window(self):
        return self.main_controller.window
    
        
    def get_status_bar(self) -> CustomStatusBar:
        return self.get_main_window().main_layout.status_bar
