import sys
import serial
import time
import threading
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout


class SerialControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.serial = serial.Serial('COM3', 9600, timeout=10)  # Adjust the timeout value as needed
        self.initUI()
        self.stop_flag = False  # Flag to control the stop action
        self.sequence_thread = None
        self.current_mode = None  # Variable to store the current mode
        self.select_mode1(None)  # Call select_mode1 to set Mode 1 as the default mode

    def initUI(self):
        self.layout = QVBoxLayout()

        mode_layout = QHBoxLayout()

        self.mode1_label = QLabel("Mode 1")
        self.mode1_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        self.mode1_label.mousePressEvent = self.select_mode1
        mode_layout.addWidget(self.mode1_label)

        self.mode2_label = QLabel("Mode 2")
        self.mode2_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        self.mode2_label.mousePressEvent = self.select_mode2
        mode_layout.addWidget(self.mode2_label)

        self.layout.addLayout(mode_layout)

        self.Min_Power_label = QLabel("Min Power:")
        self.Min_Power_input = QLineEdit()
        self.layout.addWidget(self.Min_Power_label)
        self.layout.addWidget(self.Min_Power_input)

        self.Max_Power_label = QLabel("Max Power:")
        self.Max_Power_input = QLineEdit()
        self.layout.addWidget(self.Max_Power_label)
        self.layout.addWidget(self.Max_Power_input)

        self.Power_Step_label = QLabel("Power Step:")
        self.Power_Step_input = QLineEdit()
        self.layout.addWidget(self.Power_Step_label)
        self.layout.addWidget(self.Power_Step_input)

        self.Space_Step_label = QLabel("Time space Step:")
        self.Space_Step_input = QLineEdit()
        self.layout.addWidget(self.Space_Step_label)
        self.layout.addWidget(self.Space_Step_input)

        # Change the name of the Mode 2 input label to "Percentage"
        self.Power_label_mode2 = QLabel("Power:")
        self.Power_input_mode2 = QLineEdit()
        self.layout.addWidget(self.Power_label_mode2)
        self.layout.addWidget(self.Power_input_mode2)
        self.Power_label_mode2.hide()
        self.Power_input_mode2.hide()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_sequence_thread)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_sequence_thread)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)
        self.setWindowTitle('Serial Control GUI')
        self.show()

    def select_mode1(self, event):
        print("Mode 1 selected")
        self.current_mode = 'Mode 1'
        self.show_mode1()

    def select_mode2(self, event):
        print("Mode 2 selected")
        self.current_mode = 'Mode 2'
        self.show_mode2()

    def show_mode1(self):
        self.Min_Power_label.show()
        self.Min_Power_input.show()
        self.Max_Power_label.show()
        self.Max_Power_input.show()
        self.Power_Step_label.show()
        self.Power_Step_input.show()
        self.Space_Step_label.show()
        self.Space_Step_label.show()
        self.Power_label_mode2.hide()
        self.Power_input_mode2.hide()

    def show_mode2(self):
        self.Min_Power_label.hide()
        self.Min_Power_input.hide()
        self.Max_Power_label.hide()
        self.Max_Power_input.hide()
        self.Power_Step_label.hide()
        self.Power_Step_input.hide()
        self.Space_Step_label.hide()
        self.Space_Step_input.hide()
        self.Power_input_mode2.show()
        self.Power_label_mode2.show()

    def start_sequence_thread(self):
        if self.current_mode == 'Mode 1':
            self.stop_flag = False
            self.sequence_thread = threading.Thread(target=self.start_sequence_mode1)
        elif self.current_mode == 'Mode 2':
            self.stop_flag = False
            self.sequence_thread = threading.Thread(target=self.start_sequence_mode2)

        if self.sequence_thread:
            self.sequence_thread.start()

    def start_sequence_mode1(self):
        try:
            min_power = int(self.Min_Power_input.text())
            max_power = int(self.Max_Power_input.text())
            power_step = int(self.Power_Step_input.text())
            space_step = int(self.Space_Step_input.text())

            # number_of_periods = 5  ###########################################################   SOS change number of periods here!!!!!!!!!!!!!!!!!!!!!

            max_per = (max_power / 100)
            min_per = (min_power / 100)
            min_val = int(14 + min_per * (60 - 14))
            max_val = int(14 + max_per * (60 - 14))
            val = min_val
            percentage = min_power
            iterations = int((max_power - min_power) / power_step)
            self.command("-1")
            time.sleep(3)
            while (True):
                for i in range(iterations):
                    if self.stop_flag:
                        self.command("0")  # Send '0' to ensure a graceful stop
                        return
                    print(str(percentage) + "%")
                    val = int(14 + (percentage / 100) * (60 - 14))
                    print(val)
                    self.command(str(val))
                    val += power_step
                    percentage += power_step
                    time.sleep(space_step)

                for j in range(iterations):
                    if self.stop_flag:
                        self.command("0")  # Send '0' to ensure a graceful stop
                        return
                    print(str(percentage) + "%")
                    val = int(14 + (percentage / 100) * (60 - 14))
                    print(val)
                    self.command(str(val))
                    percentage -= power_step
                    time.sleep(space_step)
                time.sleep(3)

        except ValueError:
            print("Please enter valid integer values for Percentage, Period, and Space")

    def start_sequence_mode2(self):

        try:
            self.command("-1")
            percentage = int(self.Power_input_mode2.text())  # Using the correct input field for Mode 2
            per = (percentage / 100)
            val = int(14 + per * (60 - 14))
            self.command(str(val))
            # Implement Mode 2 sequence using mode2_specific_value
            # Perform tasks related to Mode 2 using the 'mode2_specific_value'
            pass
        except ValueError:
            print("Please enter valid values for Mode 2")

    def stop_sequence_thread(self):
        self.stop_flag = True
        self.command("0")
        if self.sequence_thread:
            self.sequence_thread.join()  # Wait for the sequence thread to complete

    def command(self, value):
        self.serial.write(str.encode(value + "%"))
        time.sleep(0.1)


def main():
    app = QApplication(sys.argv)
    ex = SerialControlGUI()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
