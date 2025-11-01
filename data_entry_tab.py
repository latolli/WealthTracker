from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DataEntryTab(QWidget):
    def __init__(self, data_handler, graphs_tab):
        super().__init__()
        self.data_handler = data_handler
        self.graphs_tab = graphs_tab
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 0, 100, 100)

        # Fonts
        title_font = QFont("Arial", 16, QFont.Bold)

        # Display existing data
        title_label = QLabel("Choose data to edit or add new")
        title_label.setFont(title_font)

        self.combo = QComboBox()
        self.refresh_combo_box()
        self.combo.currentIndexChanged.connect(self.on_selection_changed)

        self.selected_item_label = QLabel("Selected: New data")

        layout.addWidget(title_label)
        layout.addWidget(self.combo)
        layout.addWidget(self.selected_item_label)

        # Form for adding & editing data
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(12)  # Add spacing between rows

        form_field_names = ["month", "mortage_loan", "other_loan", "salary", "other_income", "invested_and_loans_payed", "living_and_bills",
                            "food_expenses", "sport_culture_travel", "other_expenses", "house", "car", "bank", "investments"]
        self.assets_keys = ["house", "car", "bank", "investments"]
        self.form_fields_widgets = {}

        for f in form_field_names:
            self.form_fields_widgets[f] = {}
            input_widget = QLineEdit()
            self.form_fields_widgets[f]["input"] = input_widget

            label_text = f.capitalize().replace("_", " ")
            if f in self.assets_keys:
                label_text += " Value"
            elif f == "month":
                label_text += " (e.g., 2025-04)"

            label_widget = QLabel(label_text)

            form_layout.addRow(label_widget, input_widget)

        layout.addLayout(form_layout)

        # Save button
        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        # Delete button
        delete_button = QPushButton("Delete Data")
        delete_button.clicked.connect(self.delete_data)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def save_data(self):
        try:
            data = {}
            assets_keys = {"house", "car", "bank", "investments"}
            assets = {}

            for key, widget_dict in self.form_fields_widgets.items():
                raw_value = widget_dict["input"].text().strip()
                if key == "month":
                    data["month"] = raw_value  # Month is a string
                else:
                    value = float(raw_value)  # Attempt conversion for numeric fields
                    if key in assets_keys:
                        assets[key] = value
                    else:
                        data[key] = value
            data["assets"] = assets

            # Save data and refresh graphs
            self.data_handler.add_monthly_data(data)
            self.graphs_tab.refresh_graphs()
            self.refresh_combo_box()

            QMessageBox.information(self, "Success", "Data saved successfully!")

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numeric values.")

    def delete_data(self):
        selected_index = self.combo.currentIndex()
        if selected_index == 0:
            QMessageBox.warning(self, "Error", "No data selected to delete.")
            return

        data = self.data_handler.read_data()["monthly_data"]
        month_to_delete = data[selected_index - 1]["month"]

        # Remove the selected month data
        data.pop(selected_index - 1)
        self.data_handler.write_data({"monthly_data": data})

        # Refresh the combo box and graphs
        self.refresh_combo_box()
        self.graphs_tab.refresh_graphs()

        QMessageBox.information(self, "Success", f"Data for {month_to_delete} deleted successfully!")

    def on_selection_changed(self, index):
        # QComboBox can emit -1 during clear/add operations; guard against invalid indices
        if index is None or index < 0:
            # Treat as 'New data' selection and clear inputs
            self.selected_item_label.setText("Selected: New data")
            for widget_dict in self.form_fields_widgets.values():
                widget_dict["input"].clear()
            return

        selected_item = self.combo.currentText()
        self.selected_item_label.setText(f"Selected: {selected_item}")

        if selected_item == "New data" or index == 0:
            # Clear all inputs for new entry
            for widget_dict in self.form_fields_widgets.values():
                widget_dict["input"].clear()
            return

        # For existing entries ensure index maps to data list safely
        data_list = self.data_handler.read_data().get("monthly_data", [])
        data_index = index - 1
        if data_index < 0 or data_index >= len(data_list):
            # Out-of-range: clear inputs and avoid crash
            for widget_dict in self.form_fields_widgets.values():
                widget_dict["input"].clear()
            return

        data = data_list[data_index]
        for key, widget_dict in self.form_fields_widgets.items():
            if key == "month":
                widget_dict["input"].setText(data.get("month", ""))
            elif key in self.assets_keys:
                widget_dict["input"].setText(str(data.get("assets", {}).get(key, "")))
            else:
                widget_dict["input"].setText(str(data.get(key, "")))

    def refresh_combo_box(self):
        # Refresh the data in combo box and graphs
        updated_data = self.data_handler.read_data()["monthly_data"]
        updated_months = ["New data"] + [entry["month"] for entry in updated_data]
        self.combo.clear()
        self.combo.addItems(updated_months)
        self.combo.setCurrentIndex(0)