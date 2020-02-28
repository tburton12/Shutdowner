import sys
from PyQt5.QtWidgets import *
import datetime
import subprocess


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
        now = datetime.datetime.now()
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
        self.restart_action = QRadioButton("Restart")

        # --- Buttons section --- #
        self.reset_button = QPushButton("Reset values", self)
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_button_clicked)

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
        self.action_section_layout.addWidget(self.restart_action)
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
        """Manage scheduling action basing on options selected in form"""
        delay = self.get_action_delay()

        # Cancel scheduling if delay contains an error code
        if delay < 0:
            return

        if self.shutdown_action.isChecked():
            self.perform_action(delay=delay, flags="/s")
            self.update_status_bar("Shutdown scheduled!")

        elif self.restart_action.isChecked():
            self.perform_action(delay=delay, flags="/r")
            self.update_status_bar("Restart scheduled!")

        elif self.hibernate_action.isChecked():
            self.perform_action(delay=delay, flags="/h /f")
            self.update_status_bar("Hibernation scheduled!")

        elif self.logout_action.isChecked():
            self.perform_action(delay=delay, flags="/l")
            self.update_status_bar("Logout scheduled!")

    @staticmethod
    def perform_action(flags, delay=1):
        """Perform action with shutdown command with given parameters (for shutdown, restart etc.)"""
        # Used delayed ping to perform delay
        command = "ping -n " + str(delay) + " 127.0.0.1 > NUL 2>&1 && shutdown " + flags
        print(command)
        ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def get_action_delay(self):
        """Returns calculated action delay basing on option selected in form
        :returns calculated delay or -1 if error occurred"""

        delay = 1

        # If delay in minutes is given, convert it to seconds
        if self.action_in_time_option.isChecked():
            delay = self.minutes_spinner.value() * 60

        # If precise date is given, parse it and calculate delay in seconds
        elif self.action_at_time_option.isChecked():
            dt = self.parse_time_from_form()

            if dt is not None:
                if dt > datetime.datetime.now():
                    delay = self.seconds_delta(dt, datetime.datetime.now())
                else:
                    self.update_status_bar("Select date is future!")
                    return -1
            else:
                self.update_status_bar("Invalid datetime")
                return -1

        return delay

    def parse_time_from_form(self):
        """Reads date given in form and converts it to datetime format
        :returns parsed datetime"""

        # Read values from form
        try:
            y, mon, d = int(self.year_widget.text()), int(self.month_widget.text()), int(self.day_widget.text())
            h, m, s = int(self.hour_widget.text()), int(self.minute_widget.text()), int(self.second_widget.text())
        except ValueError as err:
            print(err)
            return None

        # Convert values into datetime format and return it
        if None not in (y, mon, d, h, m, s):
            date_time_str = str(y) + " " + str(mon) + " " + str(d) + " " + str(h) + " " + str(m) + " " + str(s)

            dt = datetime.datetime
            try:
                dt = dt.strptime(date_time_str, '%Y %m %d %H %M %S')
            except Exception as err:
                print(err)

            return dt

    @staticmethod
    def seconds_delta(dt1, dt2):
        """Calculates and returns difference between two dates in seconds.
        It considers differences in date and time.
        :returns Difference in seconds
        """
        # Get positive delta
        if dt1 > dt2:
            s = dt1 - dt2
        else:
            s = dt2 - dt1

        # Consider difference in dates
        if s.days >= 1:
            return s.seconds + s.days * 86400
        else:
            return s.seconds

    def update_status_bar(self, command):
        print(command)


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
