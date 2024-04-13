# Serial Command Tool V1.0 


Version 1.0 of this application is a tool that sends commands to a serial port at specified times based on a JSON file. It is modified from the ulcc.py control program of the [Github open source project 10032-bili/Cable-pulling-robot-arm/tree/main/ulcc](https://github.com/10032-bili/Cable-pulling-robot-arm/tree/main/ulcc), allowing either manual sending of serial commands or timed sending of command sequences through a JSON file. It also includes a JSON editor and is suitable for serial port device management and debugging scenarios.

## README
[**简体中文**](README.md)     
[**English**](README_en.md)

## Interface Selection
### Interface **serial_command_execution**
![serial_command_execution img](img/serial_command_execution_en.png)

`serial_command_execution`
- **Serial Port Management**:
  - Press the `Scan ports` button to scan.
  - Select the available serial port from the dropdown textbox next to `Select Serial Port`.
  - Configure the baud rate from the dropdown textbox next to `Baud Rate`.
  - Press the `Start` button to start serial communication.
- **Command Execution**:
  - Enter the command to be sent to the connected device in the input box.
  - Press the `Send` button to send the command.
  - Or click the `Select JSON File` button to choose a JSON command sequence.
  - Click the `Start execution` button to begin executing the command sequence.
  - The data returned from the serial port is displayed in real-time in the output textbox below.
### Interface **command_editing**
![command_editing img](img/command_editing_en.png)

`command_editing`
- **Command Editing**:
  - Enter the command sequence in the format `execution time, command to send to the serial port` into the input textbox.
  - Click `Generate JSON` to preview the json in the output textbox below.
  - Enter the json file name in the textbox to the left of the `Save JSON file` button.
  - Click the `Save JSON file` to choose the path for saving the json file.

## Running Requirements

### Running the Python Source Code

Before running this Python source code, please ensure the following are installed:
- Python 3.x ([**Download Python**](https://www.python.org/downloads/))
- `tkinter` library (usually included in Python)
- `pyserial` package

If `pyserial` is not yet installed, it can be installed using pip:

```bash
pip install pyserial
```

### Running the Windows exe Program
Download the packaged EXE program and run it on Windows.

[**EXE Program Download**](https://github.com/10032-bili/Serial-Command-Tool/releases/download/V1.0/Serial_Command_Tool.exe)

## Support
If you need help, please visit the "[Github Project 10032-bili/Serial-Command-Tool](https://github.com/10032-bili/Serial-Command-Tool)" open source page to contact the developers.

## LICENSE
This program follows the MIT license. You can view the full license in the "[**LICENSE**](LICENSE)"file.

# Caution
**This program is for learning and reference only and Do not use this program for any illegal purposes.**

* Copyright ©2024 [peidong sun](https://github.com/10032-bili).
* Distributed under MIT license.

* This program is open-source under MIT LICENSE, the original author does not have any control over the program or its derivatives and is not liable for any legal responsibilities!
## LOGO
![serial.ico](img/serial.ico)
---
Copyright ©2024 sun peidong. All Rights Reserved.
