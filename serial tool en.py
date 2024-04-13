#Distributed under MIT license.
#Copyright ©2024 Peidong Sun
#https://github.com/10032-bili/Serial-Command-Tool/
import tkinter as tk
from tkinter import ttk, filedialog
import threading
import serial
from serial.tools import list_ports
import json
import time
import base64
from tkinter import ttk, PhotoImage
class SerialCommandAPP:
    def __init__(self, master):
        self.master = master
        master.title('Serial tool v1.0 developed by ©Peidong Sun 2024')
        # List of threads managing program execution
        self.program_threads = []
        self.thread = None  # Initialize thread attribute
        # Decode the ICON base64 string

        # Create interface switch selection bar
        self.mode_var = tk.StringVar()
        self.mode_var.set("serial_command_execution")  # Default set to serial command execution mode
        self.mode_selector = ttk.Combobox(master, textvariable=self.mode_var, values=["serial_command_execution", "command_editing"])
        self.mode_selector.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.mode_selector.bind("<<ComboboxSelected>>", self.switch_mode)

        # Serial command execution frame
        self.serial_command_execution_frame = ttk.Frame(master)
        self.serial_command_execution_frame.grid(row=1, column=0, columnspan=2)
        self.create_serial_command_execution_ui(self.serial_command_execution_frame)

        # Command editing frame
        self.command_editing_frame = ttk.Frame(master)
        self.command_editing_frame.grid(row=1, column=0, columnspan=2)
        self.create_command_editing_ui(self.command_editing_frame)
        self.command_editing_frame.grid_remove()

        # Set up the closing event handler
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_serial_command_execution_ui(self, frame):
        """Serial command execution interface"""
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        self.serial_port = None
        self.running = False
        self.start_time = None  # Initialize start time attribute

        # Serial port selection and scan button
        self.port_label = ttk.Label(frame, text="Select serial port:")
        self.port_label.grid(row=0, column=0)
        self.port_combo = ttk.Combobox(frame)
        self.port_combo.grid(row=0, column=1)
        self.refresh_ports()

        self.refresh_button = ttk.Button(frame, text="Scan ports", command=self.refresh_ports)
        self.refresh_button.grid(row=0, column=2)

        # Baud rate selection
        self.baudrate_label = ttk.Label(frame, text="Baud rate:")
        self.baudrate_label.grid(row=0, column=3)
        self.baudrate_combo = ttk.Combobox(frame, values=[2400, 9600, 19200, 38400, 57600, 115200], state="readonly")
        self.baudrate_combo.grid(row=0, column=4)
        self.baudrate_combo.set("19200")

        self.start_button = ttk.Button(frame, text="Start", command=self.start_serial)
        self.start_button.grid(row=0, column=5)

        # Add text input box
        self.input_text = ttk.Entry(frame)
        self.input_text.grid(row=5, column=1, columnspan=6, padx=10, pady=10)

        # Add send button
        self.send_button = ttk.Button(frame, text='Send', command=self.send_serial)
        self.send_button.grid(row=5, column=6, columnspan=2)

        # Text box for displaying serial port data
        self.serial_output_text = tk.Text(frame, height=15, width=50)
        self.serial_output_text.grid(row=7, column=0, columnspan=8, padx=10, pady=10)

        self.select_file_button = ttk.Button(frame, text="Select JSON file", command=self.select_program_file)
        self.select_file_button.grid(row=6, column=2, padx=10, pady=10)
        # Start execution button
        self.btn_execute = ttk.Button(frame, text="Start execution", command=self.execute_program)
        self.btn_execute.grid(row=6, column=3, padx=10, pady=10)

        # Copyright information label
        self.footer_label = ttk.Label(frame, text="Copyright ©2024 Peidong Sun. All Rights Reserved.", background="gray", foreground="white")  
        self.footer_label.grid(row=10, column=0, columnspan=8, sticky="ew", pady=(10,0))

        # Set row and column weights for window size adaptation
        for i in range(8):
            frame.columnconfigure(i, weight=1)
        for i in range(7):
            frame.rowconfigure(i, weight=1)

    def switch_mode(self, event=None):
        """Switch interface mode"""
        if self.mode_var.get() == "serial_command_execution":
            self.serial_command_execution_frame.grid()
            self.command_editing_frame.grid_remove()
        elif self.mode_var.get() == "command_editing":
            self.serial_command_execution_frame.grid_remove()
            self.command_editing_frame.grid()

    def select_program_file(self):
        """Select program file and load commands"""
        self.file_path = filedialog.askopenfilename(title="Select program file", filetypes=[("JSON Files", "*.json")])
        if self.file_path:
            self.serial_output_text.delete('1.0', tk.END)
            self.program_data = self.load_instructions(self.file_path)
            self.serial_output_text.insert(tk.END, f"Selected file: {self.file_path}\n")

    def load_instructions(self, file_path):
        """Load list of commands from file"""
        with open(file_path, 'r') as file:
            return json.load(file)
            
    def execute_program(self):
        """Asynchronously execute program and update GUI"""
        if not self.program_data:
            self.serial_output_text.insert(tk.END, "Program data is empty, please load the program first.\n")
            return
        self.serial_output_text.insert(tk.END, "Starting program execution...\n")
        threading.Thread(target=self.execute_program_instructions, args=(self.program_data,), daemon=True).start()

    def execute_program_instructions(self, program_data):
        try:
            """Execute program commands in a new thread"""
            self.start_time = time.time()
            for instruction in sorted(program_data, key=lambda x: x['time']):
                while time.time() - self.start_time < instruction['time']:
                    time.sleep(0.01)

                command = instruction['command']
                # Send command
                self.send_and_log(f"{command}")
        # After all commands are executed, display a message in the GUI
            self.master.after(0, lambda: self.serial_output_text.insert(tk.END, "All commands executed\n"))
        except Exception as e:
        # If an error occurs, output the error information to the GUI
            error_msg = f"An error occurred while executing commands: {str(e)}"
            self.serial_output_text.insert(tk.END, error_msg)

    def create_command_editing_ui(self, frame):
        """Create program editing interface"""
        self.program_text = tk.Text(frame, height=10)
        self.program_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.program_text.insert(tk.END, "Enter program commands\nFormat: time (seconds), serial command content\nExample: 2,hello, world\n")

        self.generate_program_button = ttk.Button(frame, text="Generate JSON", command=self.generate_program)
        self.generate_program_button.grid(row=1, column=1, padx=10, pady=10)

        self.program_output = tk.Text(frame, height=15, width=50)
        self.program_output.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        # Add file name edit box and save button
        self.file_name_entry = ttk.Entry(frame, width=30)
        self.file_name_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.save_program_button = ttk.Button(frame, text="Save JSON file", command=self.save_program_file)
        self.save_program_button.grid(row=3, column=3, padx=10, pady=10)


        self.footer_label = ttk.Label(frame, text="Copyright ©2024 Peidong Sun. All Rights Reserved.", background="gray", foreground="white")
        self.footer_label.grid(row=8, column=0, columnspan=8, sticky="ew", pady=(10, 0))


    def generate_program(self):
        program_lines = self.program_text.get("1.0", tk.END).strip().split("\n")
        program_data = []
       
        for line in program_lines:
            parts = line.split(",")
            if len(parts) == 2:
                try:
                    time = int(parts[0].strip())  # Correctly extract and convert time from parts
                    command = parts[1].strip()    # Correctly extract command from parts
                    program_data.append({"time": time, "command": command})
                except ValueError:
                    print(f"Skipping invalid line: {line}")  # Print or log invalid line
                    continue  # Skip invalid line

        program_data.sort(key=lambda x: x["time"])
        program_document = json.dumps(program_data, indent=4)

        self.program_output.delete("1.0", tk.END)
        self.program_output.insert(tk.END, program_document)

    def save_program_file(self):
        """Save program file"""
        file_name = self.file_name_entry.get()
        if file_name:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=file_name, filetypes=[("JSON Files", "*.json")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.program_output.get("1.0", tk.END))

    def refresh_ports(self):
        """Refresh the list of available serial ports"""
        ports = list_ports.comports()
        self.port_combo['values'] = [port.device for port in ports]

    def start_serial(self):
        """Start serial communication"""
        if self.serial_port:
            self.running = False
            if self.thread:  # Check if the thread exists
                self.thread.join()
            self.serial_port.close()
            self.serial_port = None
        selected_port = self.port_combo.get()
        selected_baudrate = self.baudrate_combo.get()
        if selected_port:
            self.serial_port = serial.Serial(selected_port, baudrate=int(selected_baudrate), timeout=1)
            self.running = True
            self.thread = threading.Thread(target=self.listen_serial)
            self.thread.start()

    def listen_serial(self):
        """Listen to serial data"""
        while self.running:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode().strip()
                self.log_message(f"Received: {data}")  # Display received data
                self.master.after(0, self.log_message, f"Received: {data}")  # Update text box in the main thread

    def send_serial(self):
        text = self.input_text.get()  # Get text from the input box
        self.send_and_log(text)  # Send text to the serial port

    def send_and_log(self, message):
        """Send data and log message"""

        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write((message + "\r\n").encode())  # Send the command to the serial port

    def log_message(self, message):
        """Log message to log"""
        self.serial_output_text.insert(tk.END, message + "\n")
        self.serial_output_text.see(tk.END)

    def send_and_log_preset(self, message):
        """Send data and log message (for preset program interface)"""
        self.log_message_preset(message)  # Display message in GUI
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write((message + "\r\n").encode())  # Send data to the serial port, ensure it ends with a carriage return

    def log_message_preset(self, message):
        """Log message to log (for preset program interface)"""
        self.serial_output_text.insert(tk.END, message + "\n")
        self.serial_output_text.see(tk.END)

    def on_closing(self):
        """Handle application closing event"""
        # Stop all background threads
        if hasattr(self, 'running') and self.running:
            self.running = False
            for thread in self.program_threads:
                if thread.is_alive():
                    thread.join()

        if hasattr(self, 'serial_port') and self.serial_port:
            self.serial_port.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialCommandAPP(root)
    root.mainloop()

    # Ensure background threads are properly closed when the GUI closes
    if app.running:
        app.running = False
        if app.thread:  # Check if the thread exists
            app.thread.join()
    if app.serial_port:
        app.serial_port.close()
