import sys
from PyQt5.QtWidgets import *
from datetime import datetime


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shutdowner")
        self.setGeometry(350, 150, 400, 200)
        self.widgets()
        self.layouts()
        self.show()

    def widgets(self):
        """"Definition of used Widgets"""

        # --- Time section --- #

        # Time option radio
        self.action_in_time_option = QRadioButton("Make action in:")
        self.action_in_time_option.setChecked(True)
        self.action_at_time_option = QRadioButton("Make action at:")

        # Minute spinner
        self.minutes_spinner = QSpinBox()
        self.minutes_spinner.setSingleStep(15)

        # Date time selection widgets
        now = datetime.now()
        self.year_widget = QLineEdit(str(now.year))
        self.month_widget = QLineEdit(str(now.month))
        self.day_widget = QLineEdit(str(now.day))

        self.hour_widget = QLineEdit(str(now.hour))
        self.minute_widget = QLineEdit(str(now.minute))
        self.second_widget = QLineEdit("00")

        # --- Actions section --- #
        self.shutdown_action = QRadioButton("Shutdown")
        self.shutdown_action.setChecked(True)
        self.hibernate_action = QRadioButton("Hibernate")
        self.logout_action = QRadioButton("Logout")

        # --- Buttons section --- #
        self.reset_button = QPushButton("Reset values", self)
        self.start_button = QPushButton("Start")
        self.cancel_button = QPushButton("Cancel actions")

        # --- Others --- #
        self.frame = QFrame()
        self.frame.resize(300, 300)
        self.frame.setStyleSheet("background-color: rgb(200, 255, 255)")

        self.message_bar = QLabel()

    def layouts(self):
        """Definition of all used Layouts"""

        # ------ Parameters ------ #
        # --- Time section --- #
        self.time_section_layout = QVBoxLayout()
        self.time_section_layout.addWidget(self.frame)
        self.time_section_layout.addWidget(self.action_in_time_option)
        self.time_section_layout.addWidget(self.minutes_spinner)
        self.time_section_layout.addWidget(self.action_at_time_option)

        self.date_layout = QHBoxLayout()
        self.date_layout.addWidget(self.year_widget)
        self.date_layout.addWidget(self.month_widget)
        self.date_layout.addWidget(self.day_widget)

        self.time_layout = QHBoxLayout()
        self.time_layout.addWidget(self.hour_widget)
        self.time_layout.addWidget(self.minute_widget)
        self.time_layout.addWidget(self.second_widget)

        self.time_section_layout.addLayout(self.date_layout)
        self.time_section_layout.addLayout(self.time_layout)

        self.time_section_group = QGroupBox()
        self.time_section_group.setLayout(self.time_section_layout)

        # --- Actions section --- #
        self.action_section_layout = QVBoxLayout()
        self.action_section_layout.addWidget(self.shutdown_action)
        self.action_section_layout.addWidget(self.hibernate_action)
        self.action_section_layout.addWidget(self.logout_action)

        self.action_section_group = QGroupBox()
        self.action_section_group.setLayout(self.action_section_layout)

        # --- Parameters --- #
        self.parameters_layout = QHBoxLayout()
        self.parameters_layout.addWidget(self.time_section_group)
        self.parameters_layout.addWidget(self.action_section_group)

        # ------ Control panel ------ #
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.cancel_button)
        self.control_layout.addWidget(self.reset_button)
        self.control_layout.addWidget(self.start_button)

        # ------ Bottom bar ------#
        self.bottom_bar_layout = QHBoxLayout()
        self.bottom_bar_layout.addWidget(self.message_bar)
        self.bottom_bar_layout.addStretch()
        self.bottom_bar_layout.addWidget(QLabel("© Paweł Wrzesień"))

        # ------ Main layout ------ #
        self.main_layout = QVBoxLayout()
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.parameters_layout)
        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addLayout(self.bottom_bar_layout)
        self.setLayout(self.main_layout)

    def start_button_clicked(self):
        if self.shutdown_action.isChecked():
            self.shutdown_computer()

        elif self.hibernate_action.isChecked():
            self.hibernate_computer()

        elif self.logout_action.isChecked():
            self.logout_user()

    def shutdown_computer(self):
        pass

    def hibernate_computer(self):
        pass

    def logout_user(self):
        pass

def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
