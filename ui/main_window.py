from PyQt5.QtWidgets import QMainWindow, QTabWidget
from data_entry_tab import DataEntryTab
from ui.graphs_tab import GraphsTab

class MainWindow(QMainWindow):
    def __init__(self, data_handler, business_logic):
        super().__init__()
        self.setWindowTitle("Wealth Tracker")
        self.setGeometry(400, 50, 1200, 1000)

        self.data_handler = data_handler
        self.business_logic = business_logic

        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()

        self.set_app_style()

        # Graphs Tab
        self.graphs_tab = GraphsTab(self.business_logic)
        tabs.addTab(self.graphs_tab, "Graphs")

        # Data Entry Tab
        self.data_entry_tab = DataEntryTab(self.data_handler, self.graphs_tab)
        tabs.addTab(self.data_entry_tab, "Data Entry")

        self.setCentralWidget(tabs)

    def set_app_style(self):
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border: 2px solid white;
                padding: 10px;
                margin: 20px 0px 0px 0px;
                border-radius: 5px;
                background-color: transparent;
                font-size: 14px;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
                font-size: 14px;
                font-family: Arial;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-family: Arial;
            }
            QLineEdit {
                color: white;
                font-size: 14px;
                font-family: Arial;
            }
            QComboBox {
                color: white;
                font-size: 14px;
                font-family: Arial;
            }
        """)
