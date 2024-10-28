from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QWidget, QToolBar, QAction, QStatusBar, QListWidget, QHBoxLayout, QVBoxLayout,
    QListWidgetItem, QMessageBox, QMenu
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QPoint
import os

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.setWindowTitle("Editor de Imagem")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon(os.path.join("icons", "app_icon.png")))
        self.create_toolbar()
        self.create_status_bar()

        self.image_label = QLabel()
        self.image_label.setObjectName("image_label")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)

        central_layout = QVBoxLayout()
        central_layout.addWidget(self.image_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(central_layout)

        self.create_layers_panel()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.central_widget)
        main_layout.addWidget(self.sidebar_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.apply_styles()

    def create_toolbar(self):
        toolbar = QToolBar("Ferramentas")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        open_icon = QIcon.fromTheme("document-open")
        if open_icon.isNull():
            open_icon = QIcon("icons/open.png")
        open_action = QAction(open_icon, "Abrir Imagem", self)
        open_action.setStatusTip("Abrir uma imagem")
        open_action.triggered.connect(self.controller.load_image)
        toolbar.addAction(open_action)

        save_icon = QIcon.fromTheme("document-save")
        if save_icon.isNull():
            save_icon = QIcon("icons/save.png")
        save_action = QAction(save_icon, "Salvar Imagem", self)
        save_action.setStatusTip("Salvar a imagem atual")
        save_action.triggered.connect(self.controller.save_image)
        toolbar.addAction(save_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_layers_panel(self):
        self.layers_list = QListWidget()
        self.layers_list.setMaximumWidth(250)
        self.layers_list.setSelectionMode(QListWidget.SingleSelection)
        self.layers_list.setDragEnabled(True)
        self.layers_list.setAcceptDrops(True)
        self.layers_list.setDragDropMode(QListWidget.InternalMove)
        self.layers_list.model().rowsMoved.connect(self.on_layers_reordered)
        self.layers_list.itemChanged.connect(self.on_layer_visibility_changed)
        self.layers_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.layers_list.customContextMenuRequested.connect(self.open_context_menu)
        sidebar_layout = QVBoxLayout()
        label = QLabel("Camadas")
        label.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        sidebar_layout.addWidget(label)
        sidebar_layout.addWidget(self.layers_list)
        sidebar_layout.addStretch()

        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(sidebar_layout)

    def add_layer_to_list(self, name, visible=True):
        item = QListWidgetItem(name)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
        item.setCheckState(Qt.Checked if visible else Qt.Unchecked)
        self.layers_list.addItem(item)  # Adiciona no final da lista

    def clear_layers_list(self):
        self.layers_list.clear()

    def display_image(self, qt_image):
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))
        self.image_label.setScaledContents(True)

    def clear_image(self):
        self.image_label.clear()

    def on_layer_visibility_changed(self, item):
        index = self.layers_list.row(item)
        self.controller.toggle_layer_visibility(index)

    def on_layers_reordered(self, source_parent, source_start, source_end, dest_parent, dest_row):
        self.controller.on_layers_reordered(source_start, dest_row)
        self.display_image(self.controller.processor.get_composited_image())

    def delete_layer(self):
        selected_items = self.layers_list.selectedItems()
        if selected_items:
            current_item = selected_items[0]
            current_row = self.layers_list.row(current_item)
            layer_name = current_item.text()

            reply = QMessageBox.question(
                self, 'Confirmar Remoção',
                f"Tem certeza que deseja remover a camada '{layer_name}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.layers_list.takeItem(current_row)
                self.controller.delete_layer(current_row)
        else:
            QMessageBox.information(self, "Nenhuma Camada Selecionada", "Por favor, selecione uma camada para remover.")

    def open_context_menu(self, position):
        item = self.layers_list.itemAt(position)
        if item:
            context_menu = QMenu(self)
            remove_action = context_menu.addAction("Remover Camada")

            apply_blur_action = context_menu.addAction("Aplicar Blur")
            apply_gaussian_blur_action = context_menu.addAction("Aplicar Gaussian Blur")
            apply_median_blur_action = context_menu.addAction("Aplicar blur mediano")
            
            action = context_menu.exec_(self.layers_list.viewport().mapToGlobal(position))
            if action == remove_action:
                current_row = self.layers_list.row(item)
                layer_name = item.text()

                reply = QMessageBox.question(
                    self, 'Confirmar Remoção',
                    f"Tem certeza que deseja remover a camada '{layer_name}'?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.layers_list.takeItem(current_row)
                    self.controller.delete_layer(current_row)
            elif action == apply_blur_action:
                current_row = self.layers_list.row(item)
                self.controller.apply_blur(layer_index=current_row)
            elif action == apply_gaussian_blur_action:
                current_row = self.layers_list.row(item)
                self.controller.apply_gaussian_blur(layer_index=current_row)
            elif action == apply_median_blur_action:
                current_row = self.layers_list.row(item)
                self.controller.apply_median_blur(layer_index=current_row)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QLabel#image_label {
                background-color: #2E2E2E;
                border: none;
            }
            QListWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3E3E3E;
            }
            QToolBar {
                background-color: #2E2E2E;
                border-bottom: 1px solid #3E3E3E;
            }
            QToolButton {
                background-color: transparent;
                border: none;
            }
            QToolButton:hover {
                background-color: #3E3E3E;
            }
            QStatusBar {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
