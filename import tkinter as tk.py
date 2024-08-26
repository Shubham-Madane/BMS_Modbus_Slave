import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class SerialReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BMS Modbus Slave")
        self.geometry("600x900")

        # Box for Received Data
        tk.Label(self, text="Received Data:").pack(pady=5)
        self.received_data_text = tk.Text(self, height=5, width=45, state="disabled")
        self.received_data_text.pack(padx=10, pady=5)

        # Frame for the 5 small boxes
        tk.Label(self, text="ID").pack(pady=1)
        self.received_data_text = tk.Text(self, height=1, width=10, state="disabled")
        self.received_data_text.pack(padx=0, pady=1)
        tk.Label(self, text="FC").pack(pady=0)
        self.received_data_text = tk.Text(self, height=1, width=10, state="disabled")
        self.received_data_text.pack(padx=1, pady=2)

        frame_small_boxes = tk.Frame(self)
        frame_small_boxes.pack(pady=10)

        self.id_var = tk.StringVar()
        self.fc_var = tk.StringVar()
        self.first_register_req_var = tk.StringVar()
        self.no_of_register_var = tk.StringVar()
        self.crc_var = tk.StringVar()

        # Creating the labels and entry boxes
        self.create_small_box(frame_small_boxes, "ID:", self.id_var, 0)
        self.create_small_box(frame_small_boxes, "FC:", self.fc_var, 1)
        self.create_small_box(frame_small_boxes, "1st Register Req:", self.first_register_req_var, 2)
        self.create_small_box(frame_small_boxes, "No of Register:", self.no_of_register_var, 3)
        self.create_small_box(frame_small_boxes, "CRC:", self.crc_var, 4)

        # Match indicators (Green buttons)
        frame_match_indicators = tk.Frame(self)
        frame_match_indicators.pack(pady=10)

        self.create_match_indicator(frame_match_indicators, 0)
        self.create_match_indicator(frame_match_indicators, 1)
        self.create_match_indicator(frame_match_indicators, 2)
        self.create_match_indicator(frame_match_indicators, 3)
        self.create_match_indicator(frame_match_indicators, 4)

        # Dropdown menus for COM port, baud rate, data bits, stop bits, and parity
        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.com_port = tk.StringVar()
        self.baud_rate = tk.StringVar(value="9600")
        self.data_bits = tk.StringVar(value="8")
        self.stop_bits = tk.StringVar(value="1")
        self.parity = tk.StringVar(value="None")

        # COM Port Selection
        ports = serial.tools.list_ports.comports()
        com_port_options = [port.device for port in ports]
        tk.Label(frame, text="COM Port:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.com_port_menu = ttk.Combobox(frame, textvariable=self.com_port, values=com_port_options)
        self.com_port_menu.grid(row=0, column=1, padx=10, pady=5)

        # Baud Rate Selection
        tk.Label(frame, text="Baud Rate:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        baud_rate_options = ["9600", "14400", "19200", "38400", "57600", "115200"]
        self.baud_rate_menu = ttk.Combobox(frame, textvariable=self.baud_rate, values=baud_rate_options)
        self.baud_rate_menu.grid(row=1, column=1, padx=10, pady=5)

        # Data Bits Selection
        tk.Label(frame, text="Data Bits:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        data_bits_options = ["5", "6", "7", "8"]
        self.data_bits_menu = ttk.Combobox(frame, textvariable=self.data_bits, values=data_bits_options)
        self.data_bits_menu.grid(row=2, column=1, padx=10, pady=5)

        # Stop Bits Selection
        tk.Label(frame, text="Stop Bits:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        stop_bits_options = ["1", "1.5", "2"]
        self.stop_bits_menu = ttk.Combobox(frame, textvariable=self.stop_bits, values=stop_bits_options)
        self.stop_bits_menu.grid(row=3, column=1, padx=10, pady=5)

        # Parity Selection
        tk.Label(frame, text="Parity:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        parity_options = ["None", "Even", "Odd", "Mark", "Space"]
        self.parity_menu = ttk.Combobox(frame, textvariable=self.parity, values=parity_options)
        self.parity_menu.grid(row=4, column=1, padx=10, pady=5)

        # Button to connect to the serial port
        self.connect_button = tk.Button(self, text="Connect", command=self.connect_serial)
        self.connect_button.pack(pady=20)

        # Box for Logs
        tk.Label(self, text="Logs:").pack(pady=5)
        self.logs_text = tk.Text(self, height=5, width=70, state="disabled")
        self.logs_text.pack(padx=10, pady=5)

    def create_small_box(self, parent, label_text, variable, row):
        tk.Label(parent, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(parent, textvariable=variable, width=20).grid(row=row, column=1, padx=5, pady=5)

    def create_match_indicator(self, parent, row):
        match_button = tk.Button(parent, text="✓", bg="green", width=3, state="disabled")
        match_button.grid(row=row, column=0, padx=5, pady=5)

    def connect_serial(self):
        try:
            # Map parity from string to serial.Parity constant
            parity_dict = {
                "None": serial.PARITY_NONE,
                "Even": serial.PARITY_EVEN,
                "Odd": serial.PARITY_ODD,
                "Mark": serial.PARITY_MARK,
                "Space": serial.PARITY_SPACE
            }

            # Open the serial connection
            self.serial_connection = serial.Serial(
                port=self.com_port.get(),
                baudrate=int(self.baud_rate.get()),
                bytesize=int(self.data_bits.get()),
                stopbits=float(self.stop_bits.get()),
                parity=parity_dict[self.parity.get()],
                timeout=1
            )

            self.log_message("Connected to " + self.com_port.get())

            self.after(100, self.read_serial)  # Start reading serial data

        except Exception as e:
            self.log_message(f"Error: {e}")

    def read_serial(self):
        if self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline().decode('utf-8').strip()
                if data:
                    self.display_received_data(data)
            except Exception as e:
                self.log_message(f"Read error: {e}")

            self.after(100, self.read_serial)

    def display_received_data(self, data):
        self.received_data_text.config(state="normal")
        self.received_data_text.insert(tk.END, data + "\n")
        self.received_data_text.config(state="disabled")

    def log_message(self, message):
        self.logs_text.config(state="normal")
        self.logs_text.insert(tk.END, message + "\n")
        self.logs_text.config(state="disabled")

if __name__ == "__main__":
    app = SerialReaderApp()
    app.mainloop()
