#Distributed under MIT license.
#Copyright ©2024 孙佩东
#https://github.com/10032-bili/Serial-Command-Tool/
import tkinter as tk
from tkinter import ttk, filedialog
import threading
import serial
from serial.tools import list_ports
import json
import time
class SerialCommandAPP:
    def __init__(self, master):
        self.master = master
        master.title('Serial tool v1.0 developed by ©孙佩东 2024')
        # 管理程序执行的线程列表
        self.program_threads = []
        self.thread = None  # 初始化线程属性

        # 创建界面切换选择栏
        self.mode_var = tk.StringVar()
        self.mode_var.set("serial_command_execution")  # 默认设置为串口命令执行模式
        self.mode_selector = ttk.Combobox(master, textvariable=self.mode_var, values=["serial_command_execution", "command_editing"])
        self.mode_selector.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.mode_selector.bind("<<ComboboxSelected>>", self.switch_mode)

        # 串口命令执行框架
        self.serial_command_execution_frame = ttk.Frame(master)
        self.serial_command_execution_frame.grid(row=1, column=0, columnspan=2)
        self.create_serial_command_execution_ui(self.serial_command_execution_frame)

        # 命令编辑框架
        self.command_editing_frame = ttk.Frame(master)
        self.command_editing_frame.grid(row=1, column=0, columnspan=2)
        self.create_command_editing_ui(self.command_editing_frame)
        self.command_editing_frame.grid_remove()

        # 设置关闭事件处理器
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_serial_command_execution_ui(self, frame):
        """串口命令执行界面"""
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        self.serial_port = None
        self.running = False
        self.start_time = None  # 初始化开始时间属性

        # 串口选择与扫描按钮
        self.port_label = ttk.Label(frame, text="选择串口:")
        self.port_label.grid(row=0, column=0)
        self.port_combo = ttk.Combobox(frame)
        self.port_combo.grid(row=0, column=1)
        self.refresh_ports()

        self.refresh_button = ttk.Button(frame, text="扫描串口", command=self.refresh_ports)
        self.refresh_button.grid(row=0, column=2)

        # 波特率选择
        self.baudrate_label = ttk.Label(frame, text="波特率:")
        self.baudrate_label.grid(row=0, column=3)
        self.baudrate_combo = ttk.Combobox(frame, values=[2400, 9600, 19200, 38400, 57600, 115200], state="readonly")
        self.baudrate_combo.grid(row=0, column=4)
        self.baudrate_combo.set("19200")

        self.start_button = ttk.Button(frame, text="启动", command=self.start_serial)
        self.start_button.grid(row=0, column=5)

        # 添加文本输入框
        self.input_text = ttk.Entry(frame)
        self.input_text.grid(row=5, column=1, columnspan=6, padx=10, pady=10)

        # 添加发送按钮
        self.send_button = ttk.Button(frame, text='发送', command=self.send_serial)
        self.send_button.grid(row=5, column=6, columnspan=2)

        # 文本框用于显示串口数据
        self.serial_output_text = tk.Text(frame, height=15, width=50)
        self.serial_output_text.grid(row=7, column=0, columnspan=8, padx=10, pady=10)

        self.select_file_button = ttk.Button(frame, text="选择JOSN文件", command=self.select_program_file)
        self.select_file_button.grid(row=6, column=2, padx=10, pady=10)
        # 开始执行按钮
        self.btn_execute = ttk.Button(frame, text="开始执行", command=self.execute_program)
        self.btn_execute.grid(row=6, column=3, padx=10, pady=10)

        # 版权信息标签
        self.footer_label = ttk.Label(frame, text="Copyright ©2024 孙佩东. All Rights Reserved.", background="gray", foreground="white")  
        self.footer_label.grid(row=10, column=0, columnspan=8, sticky="ew", pady=(10,0))

        # 设置行列权重以自适应窗口大小
        for i in range(8):
            frame.columnconfigure(i, weight=1)
        for i in range(7):
            frame.rowconfigure(i, weight=1)

    def switch_mode(self, event=None):
        """切换界面模式"""
        if self.mode_var.get() == "serial_command_execution":
            self.serial_command_execution_frame.grid()
            self.command_editing_frame.grid_remove()
        elif self.mode_var.get() == "command_editing":
            self.serial_command_execution_frame.grid_remove()
            self.command_editing_frame.grid()

    def select_program_file(self):
        """选择程序文件并加载指令"""
        self.file_path = filedialog.askopenfilename(title="选择程序文件", filetypes=[("JSON Files", "*.json")])
        if self.file_path:
            self.serial_output_text.delete('1.0', tk.END)
            self.program_data = self.load_instructions(self.file_path)
            self.serial_output_text.insert(tk.END, f"选定文件: {self.file_path}\n")

    def load_instructions(self, file_path):
        """从文件中加载指令列表"""
        with open(file_path, 'r') as file:
            return json.load(file)
            
    def execute_program(self):
        """异步执行程序并更新GUI"""
        if not self.program_data:
            self.serial_output_text.insert(tk.END, "程序数据为空，请先加载程序。\n")
            return
        self.serial_output_text.insert(tk.END, "开始执行程序...\n")
        threading.Thread(target=self.execute_program_instructions, args=(self.program_data,), daemon=True).start()

    def execute_program_instructions(self, program_data):
        try:
            """在新线程中执行程序指令"""
            self.start_time = time.time()
            for instruction in sorted(program_data, key=lambda x: x['time']):
                while time.time() - self.start_time < instruction['time']:
                    time.sleep(0.01)

                command = instruction['command']
                # 发送命令
                self.send_and_log(f"{command}")
        # 所有指令执行完毕后，在 GUI 中显示信息
            self.master.after(0, lambda: self.serial_output_text.insert(tk.END, "所有指令执行完毕\n"))
        except Exception as e:
        # 如果出现错误，将错误信息输出到 GUI
            error_msg = f"执行指令时出现错误: {str(e)}"
            self.serial_output_text.insert(tk.END, error_msg)

    def create_command_editing_ui(self, frame):
        """创建程序编辑界面"""
        self.program_text = tk.Text(frame, height=10)
        self.program_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.program_text.insert(tk.END, "输入程序指令\n格式为：时间(秒)串口命令内容\n例如：2,hello, world\n")

        self.generate_program_button = ttk.Button(frame, text="生成JSON", command=self.generate_program)
        self.generate_program_button.grid(row=1, column=1, padx=10, pady=10)

        self.program_output = tk.Text(frame, height=15, width=50)
        self.program_output.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        # 添加文件名编辑框和保存按钮
        self.file_name_entry = ttk.Entry(frame, width=30)
        self.file_name_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.save_program_button = ttk.Button(frame, text="保存JSON文件", command=self.save_program_file)
        self.save_program_button.grid(row=3, column=3, padx=10, pady=10)


        self.footer_label = ttk.Label(frame, text="Copyright ©2024 孙佩东. All Rights Reserved.", background="gray", foreground="white")
        self.footer_label.grid(row=8, column=0, columnspan=8, sticky="ew", pady=(10, 0))


    def generate_program(self):
        program_lines = self.program_text.get("1.0", tk.END).strip().split("\n")
        program_data = []
       
        for line in program_lines:
            parts = line.split(",")
            if len(parts) == 2:
                try:
                    time = int(parts[0].strip())  # 从parts正确提取和转换时间
                    command = parts[1].strip()    # 从parts正确提取命令
                    program_data.append({"time": time, "command": command})
                except ValueError:
                    print(f"跳过无效行: {line}")  # 打印或记录无效行
                    continue  # 跳过无效行

        program_data.sort(key=lambda x: x["time"])
        program_document = json.dumps(program_data, indent=4)

        self.program_output.delete("1.0", tk.END)
        self.program_output.insert(tk.END, program_document)

    def save_program_file(self):
        """保存程序文件"""
        file_name = self.file_name_entry.get()
        if file_name:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=file_name, filetypes=[("JSON Files", "*.json")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.program_output.get("1.0", tk.END))

    def refresh_ports(self):
        """刷新可用串口列表"""
        ports = list_ports.comports()
        self.port_combo['values'] = [port.device for port in ports]

    def start_serial(self):
        """启动串口通信"""
        if self.serial_port:
            self.running = False
            if self.thread:  # 检查线程是否存在
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
        """监听串口数据"""
        while self.running:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode().strip()
                self.log_message(f"接收: {data}")  # 显示接收到的数据
                self.master.after(0, self.log_message, f"接收: {data}")  # 在主线程更新文本框

    def send_serial(self):
        text = self.input_text.get()  # 获取输入框中的文本
        self.send_and_log(text)  # 发送文本到串口

    def send_and_log(self, message):
        """发送数据并记录消息"""

        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write((message + "\r\n").encode())  # 将命令发送到串口

    def log_message(self, message):
        """记录消息到日志"""
        self.serial_output_text.insert(tk.END, message + "\n")
        self.serial_output_text.see(tk.END)

    def send_and_log_preset(self, message):
        """发送数据并记录日志（用于预设程序界面）"""
        self.log_message_preset(message)  # 在GUI中显示消息
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write((message + "\r\n").encode())  # 向串口发送数据，确保以回车结尾

    def log_message_preset(self, message):
        """记录消息到日志（用于预设程序界面）"""
        self.serial_output_text.insert(tk.END, message + "\n")
        self.serial_output_text.see(tk.END)

    def on_closing(self):
        """处理应用关闭事件"""
        # 停止所有后台线程
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

    # 当GUI关闭时，确保后台线程也被正确关闭
    if app.running:
        app.running = False
        if app.thread:  # 检查线程是否存在
            app.thread.join()
    if app.serial_port:
        app.serial_port.close()