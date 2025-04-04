import sys
import serial
import time
import threading
import tkinter as tk
from tkinter import ttk

class SerialControlGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.serial = None
        self.stop_flag = False
        self.sequence_thread = None
        self.current_mode = None
        self.initUI()
        self.select_mode1(None)

    def initUI(self):
        self.title('Serial Control GUI')
        self.geometry('400x300')  # Fixed window size

        # Connection tab
        connection_tab = ttk.LabelFrame(self, text="Connection")
        connection_tab.pack(fill='both', expand=True)

        self.com_port_label = ttk.Label(connection_tab, text="COM Port:")
        self.com_port_entry = ttk.Entry(connection_tab)
        self.com_port_label.grid(row=0, column=0, sticky="e")
        self.com_port_entry.grid(row=0, column=1)

        self.connect_button = ttk.Button(connection_tab, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=1, column=0, columnspan=2)

        # Main tab
        main_tab = ttk.LabelFrame(self, text="Main")
        main_tab.pack(fill='both', expand=True)

        mode_frame = ttk.Frame(main_tab)
        mode_frame.grid(row=0, column=0)

        self.mode1_label = ttk.Label(mode_frame, text="Mode 1")
        self.mode1_label.configure(style="Mode.TLabel")
        self.mode1_label.bind('<Button-1>', self.select_mode1)
        self.mode1_label.grid(row=0, column=0)

        self.mode2_label = ttk.Label(mode_frame, text="Mode 2")
        self.mode2_label.configure(style="Mode.TLabel")
        self.mode2_label.bind('<Button-1>', self.select_mode2)
        self.mode2_label.grid(row=0, column=1)

        self.Min_Power_label = ttk.Label(main_tab, text="Min Power:")
        self.Min_Power_input = ttk.Entry(main_tab)
        self.Min_Power_label.grid(row=1, column=0, sticky="e")
        self.Min_Power_input.grid(row=1, column=1)

        self.Max_Power_label = ttk.Label(main_tab, text="Max Power:")
        self.Max_Power_input = ttk.Entry(main_tab)
        self.Max_Power_label.grid(row=2, column=0, sticky="e")
        self.Max_Power_input.grid(row=2, column=1)

        self.Power_Step_label = ttk.Label(main_tab, text="Power Step:")
        self.Power_Step_input = ttk.Entry(main_tab)
        self.Power_Step_label.grid(row=3, column=0, sticky="e")
        self.Power_Step_input.grid(row=3, column=1)

        self.Space_Step_label = ttk.Label(main_tab, text="Time space Step:")
        self.Space_Step_input = ttk.Entry(main_tab)
        self.Space_Step_label.grid(row=4, column=0, sticky="e")
        self.Space_Step_input.grid(row=4, column=1)

        # Change the name of the Mode 2 input label to "Percentage"
        self.Power_label_mode2 = ttk.Label(main_tab, text="Power:")
        self.Power_input_mode2 = ttk.Entry(main_tab)
        self.Power_label_mode2.grid(row=5, column=0, sticky="e")
        self.Power_input_mode2.grid(row=5, column=1)
        self.Power_label_mode2.grid_remove()
        self.Power_input_mode2.grid_remove()

        self.start_button = ttk.Button(main_tab, text="Start", command=self.start_sequence_thread)
        self.start_button.grid(row=6, column=0, columnspan=2)

        self.stop_button = ttk.Button(main_tab, text="Stop", command=self.stop_sequence_thread)
        self.stop_button.grid(row=7, column=0, columnspan=2)

        self.style = ttk.Style()
        self.style.configure("Mode.TLabel", borderwidth=1, padding=10)

    def connect_serial(self):
        com_port = self.com_port_entry.get()
        try:
            self.serial = serial.Serial(com_port, 9600, timeout=10)
            print(f"Connected to {com_port}")
        except Exception as e:
            print(f"Error connecting to {com_port}: {e}")

    def select_mode1(self, event):
        print("Mode 1 selected")
        self.current_mode = 'Mode 1'
        self.show_mode1()

    def select_mode2(self, event):
        print("Mode 2 selected")
        self.current_mode = 'Mode 2'
        self.show_mode2()

    def show_mode1(self):
        self.Power_label_mode2.grid_remove()
        self.Power_input_mode2.grid_remove()
        self.Min_Power_label.grid()
        self.Min_Power_input.grid()
        self.Max_Power_label.grid()
        self.Max_Power_input.grid()
        self.Power_Step_label.grid()
        self.Power_Step_input.grid()
        self.Space_Step_label.grid()
        self.Space_Step_input.grid()

    def show_mode2(self):
        self.Min_Power_label.grid_remove()
        self.Min_Power_input.grid_remove()
        self.Max_Power_label.grid_remove()
        self.Max_Power_input.grid_remove()
        self.Power_Step_label.grid_remove()
        self.Power_Step_input.grid_remove()
        self.Space_Step_label.grid_remove()
        self.Space_Step_input.grid_remove()
        self.Power_input_mode2.grid()
        self.Power_label_mode2.grid()

    def start_sequence_thread(self):
        if not self.serial:
            print("Please connect to a COM port first.")
            return

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
            min_power = int(self.Min_Power_input.get())
            max_power = int(self.Max_Power_input.get())
            power_step = int(self.Power_Step_input.get())
            space_step = int(self.Space_Step_input.get())

            max_per = (max_power/ 100)
            min_per = (min_power/100)
            min_val = int(14 + min_per * (60 - 14))
            max_val = int(14 + max_per * (60 - 14))
            val = min_val
            percentage = min_power
            iterations = int((max_power-min_power)/power_step)
            self.command("-1")
            time.sleep(3)
            while True:
                for _ in range(iterations):
                    if self.stop_flag:
                        self.command("0")
                        return
                    print(str(percentage)+"%")
                    val = int(14 + (percentage/100) * (60 - 14))
                    print(val)
                    self.command(str(val))
                    val += power_step
                    percentage += power_step
                    time.sleep(space_step)

                for _ in range(iterations):
                    if self.stop_flag:
                        self.command("0")
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
            percentage = int(self.Power_input_mode2.get())  # Using the correct input field for Mode 2
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
            self.sequence_thread.join()

    def command(self, value):
        if self.serial:
            self.serial.write(str.encode(value + "%"))
            time.sleep(0.1)

    def on_close(self):
        self.stop_sequence_thread()
        if self.serial:
            self.serial.close()
        self.destroy()

def main():
    app = SerialControlGUI()
    app.mainloop()

if __name__ == '__main__':
    main()
