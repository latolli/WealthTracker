import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.data_handler import DataHandler
from business_logic import BusinessLogic
import qdarktheme

def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    # Initialize data handler and business logic
    data_handler = DataHandler("assets/data.json")
    business_logic = BusinessLogic(data_handler)

    # Create and show the main window
    main_window = MainWindow(data_handler, business_logic)
    main_window.show()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()