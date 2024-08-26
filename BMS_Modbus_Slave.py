import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class SerialReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Serial Port Reader")
        self.geometry("400x300")

        # Dropdown menus for COM port, baud rate, data bits, stop bits, and parity
        self.com_port = tk.StringVar()
        self.baud_rate = tk.StringVar(value="9600")
        self.data_bits = tk.StringVar(value="8")
        self.stop_bits = tk.StringVar(value="1")
        self.parity = tk.StringVar(value="None")

        # COM Port Selection
        ports = serial.tools.list_ports.comports()
        com_port_options = [port.device for port in ports]
        tk.Label(self, text="COM Port:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.com_port_menu = ttk.Combobox(self, textvariable=self.com_port, values=com_port_options)
        self.com_port_menu.grid(row=0, column=1, padx=10, pady=5)

        # Baud Rate Selection
        tk.Label(self, text="Baud Rate:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        baud_rate_options = ["9600", "14400", "19200", "38400", "57600", "115200"]
        self.baud_rate_menu = ttk.Combobox(self, textvariable=self.baud_rate, values=baud_rate_options)
        self.baud_rate_menu.grid(row=1, column=1, padx=10, pady=5)

        # Data Bits Selection
        tk.Label(self, text="Data Bits:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        data_bits_options = ["5", "6", "7", "8"]
        self.data_bits_menu = ttk.Combobox(self, textvariable=self.data_bits, values=data_bits_options)
        self.data_bits_menu.grid(row=2, column=1, padx=10, pady=5)

        # Stop Bits Selection
        tk.Label(self, text="Stop Bits:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        stop_bits_options = ["1", "1.5", "2"]
        self.stop_bits_menu = ttk.Combobox(self, textvariable=self.stop_bits, values=stop_bits_options)
        self.stop_bits_menu.grid(row=3, column=1, padx=10, pady=5)

        # Parity Selection
        tk.Label(self, text="Parity:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        parity_options = ["None", "Even", "Odd", "Mark", "Space"]
        self.parity_menu = ttk.Combobox(self, textvariable=self.parity, values=parity_options)
        self.parity_menu.grid(row=4, column=1, padx=10, pady=5)

        # Button to connect to the serial port
        self.connect_button = tk.Button(self, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Text box to display serial data
        self.output_text = tk.Text(self, height=8, width=45, state="disabled")
        self.output_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

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

            self.output_text.config(state="normal")
            self.output_text.insert(tk.END, "Connected to " + self.com_port.get() + "\n")
            self.output_text.config(state="disabled")

            self.after(100, self.read_serial)  # Start reading serial data

        except Exception as e:
            self.output_text.config(state="normal")
            self.output_text.insert(tk.END, f"Error: {e}\n")
            self.output_text.config(state="disabled")

    def read_serial(self):
        if self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline().decode('utf-8').strip()
                if data:
                    self.output_text.config(state="normal")
                    self.output_text.insert(tk.END, data + "\n")
                    self.output_text.config(state="disabled")
            except Exception as e:
                self.output_text.config(state="normal")
                self.output_text.insert(tk.END, f"Read error: {e}\n")
                self.output_text.config(state="disabled")

            self.after(100, self.read_serial)

if __name__ == "__main__":
    app = SerialReaderApp()
    app.mainloop()
