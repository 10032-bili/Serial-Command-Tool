# Serial Command Tool V1.0

本应用1.0版本是一个可以根据josn文件设定时间和内容，由[Github开源项目 10032-bili/Cable-pulling-robot-arm/tree/main/ulcc](https://github.com/10032-bili/Cable-pulling-robot-arm/tree/main/ulcc)的ulcc上位机控制程序修改而来，是一种按照规定时间向串口发送命令的工具，可选手动发送串口命令和通过JSON文件定时发送命令序列。并附带json编辑器，适用于串口应用设备管理和调试场景。

## README
[**简体中文**](README.md)     
 [**English**](README_en.md)
## 功能
### 界面《serial_command_execution》
![serial_command_execution img](img/serial_command_execution.png)

serial_command_execution
- **串口管理**：
  - 扫描并选择可用的串口。
  - 配置波特率。
  - 启动和停止串口通信。
- **命令执行**：
  - 向连接的设备发送单个命令。
  - 或者从JSON文件执行命令序列。
  - 实时显示串口回传的数据。
- **文件处理**：
  - 打开对话框选择加载和保存命令序列的文件
### 界面《command_editing》
![command_editing img](img/command_editing.png)

command_editing img
- **命令编辑**：
  - 创建和编辑命令序列。
  - 生成并保存这些序列到JSON格式。

## 前置条件

### 运行python源码

在运行此python源码之前，请确保安装了以下内容：
- Python 3.x
- `tkinter`库（通常包含在Python中）
- `pyserial`包

如果尚未安装`pyserial`，可以使用pip进行安装：

```bash
pip install pyserial
```
### 运行windows exe程序
下载封包好的EXE程序并在Windows上运行即可。

[**EXE程序下载**](https://github.com/10032-bili/Serial-Command-Tool/Serial_Command_Tool.exe)

## 支持
  如需要帮助，请访问[Github项目 10032-bili/Serial-Command-Tool](https://github.com/10032-bili/Serial-Command-Tool)项目开源界面联系开发者。
## LICENSE
本程序遵循MIT许可证，您可以在[**LICENSE**](LICENSE)文件中查看完整的许可证文本。


# 注意
**本程序仅供学习参考，请勿用于非法用途。**

Distributed under MIT license. Copyright ©2024 Peidong Sun.

本程序基于MIT开源，原作者对程序或衍生程序没有任何控制权力，不负任何法律责任！
* Copyright ©2024 孙佩东. All Rights Reserved.
