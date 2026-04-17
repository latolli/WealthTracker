from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QSlider, QCheckBox
from PyQt5.QtGui import QFont

global_settings = {
    "time_range":{
        "label": "Time Range (months)",
        "value": 0,
        "max": 48,
        "min": 0
    },
    "private_mode":{
        "label": "Private Mode",
        "value": 0,
        "max": 1,
        "min": 0
    }
}

class SettingsTab(QWidget):
    def __init__(self, graphs_tab, assets_tab):
        super().__init__()
        self.graphs_tab = graphs_tab
        self.assets_tab = assets_tab
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(300, 30, 300, 100)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Fonts
        title_font = QFont("Arial", 16, QFont.Bold)

        # Display existing data
        title_label = QLabel("Settings")
        title_label.setFont(title_font)

        layout.addWidget(title_label)

        # Form for editing settings
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 25, 0, 25)
        form_layout.setVerticalSpacing(12)  # Add spacing between rows

        self.form_fields_widgets = {}

        for key in global_settings.keys():
            self.form_fields_widgets[key] = {}
            label_text = key.capitalize().replace("_", " ")
            entry_widget = QWidget()
            row_layout = QHBoxLayout(entry_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)

            setting = global_settings[key]
            if setting["min"] == 0 and setting["max"] == 1:
                checkbox = QCheckBox()
                checkbox.setChecked(bool(setting["value"]))
                row_layout.addWidget(checkbox)
                form_layout.addRow(QLabel(label_text), entry_widget)

                self.form_fields_widgets[key]["checkbox"] = checkbox
            else:
                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(setting["min"])
                slider.setMaximum(setting["max"])
                slider.setValue(setting["value"])
                slider.setTickInterval(1)
                slider.setTickPosition(QSlider.TicksBelow)

                value_label = QLabel(str(slider.value()))
                value_label.setFixedWidth(30)
                value_label.setAlignment(Qt.AlignCenter)

                slider.valueChanged.connect(
                    lambda value, label=value_label: label.setText(str(value))
                )

                row_layout.addWidget(slider)
                row_layout.addWidget(value_label)
                form_layout.addRow(QLabel(label_text), entry_widget)

                self.form_fields_widgets[key]["slider"] = slider
                self.form_fields_widgets[key]["value_label"] = value_label

        layout.addLayout(form_layout)

        # Save button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        # Reset button
        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self.reset_data)
        layout.addWidget(reset_button)

        self.setLayout(layout)

    def save_data(self):
        try:
            for key, widget_dict in self.form_fields_widgets.items():
                if "checkbox" in widget_dict:
                    value = 1 if widget_dict["checkbox"].isChecked() else 0
                else:
                    value = widget_dict["slider"].value()
                global_settings[key]["value"] = value

            self.reset_graphs_and_assets()
            QMessageBox.information(self, "Success", "Data saved successfully!")

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid values.")

    def reset_data(self):
        # Reset settings to default values
        for key in global_settings.keys():
            default_value = global_settings[key]["min"]
            global_settings[key]["value"] = default_value
            widget_dict = self.form_fields_widgets[key]
            if "checkbox" in widget_dict:
                widget_dict["checkbox"].setChecked(bool(default_value))
            else:
                widget_dict["slider"].setValue(default_value)

        self.reset_graphs_and_assets()
        QMessageBox.information(self, "Success", "Settings reset to defaults!")

    def reset_graphs_and_assets(self):
        # Refresh graphs and assets to reflect current settings
        self.graphs_tab.refresh_graphs()
        self.assets_tab.refresh_assets()
