# MHWS 自动备份工具
# MHWS Auto Backup Tool

## 简介
本工具因为作者近一百小时的游戏存档坏档，上网搜索半天无果只能重开新档白忙活而红温编写，用于自动备份《怪物猎人：荒野》的游戏存档（同时支持自定义以对其它游戏存档进行备份、应用工作成果留档，详情可在下方配置工具页面查看）。通过Windows自带的配置任务计划程序，工具可伴随系统启动自动在后台运行，检测游戏（程序）启动并自动备份存档。目前只支持Windows系统。

## Introduction (For instructions in English, please scroll to the bottom half of the page.)
This tool was developed by the author after losing nearly 100 hours of game progress due to corrupted save files, with no solution found online, leading to the frustration of starting over. It is designed to automatically back up save files for *Monster Hunter: Wilds* (and can be customized to back up save files for other games or work-related files—details can be found in the configuration tool section below). By using Windows' built-in Task Scheduler, the tool can run automatically in the background upon system startup, detecting when the game (or program) is launched and automatically backing up the save files. Currently, only Windows systems are supported.

## 功能
- **自动备份**：检测游戏运行状态，自动备份存档文件。
- **图形界面配置**：提供图形界面（GUI）工具，方便用户修改配置文件。
- **日志记录**：提供日志记录，方便追溯脚本是否正常启动、运行。
- **单实例运行**：确保同一时间只有一个备份程序运行，避免冗余程序占用系统资源。

## 使用说明

### 1. 准备工作
- 从[release](https://github.com/acatsamaovo/AutoBackupForMHWS/releases/tag/v1.0.0)中下载zip压缩包
- 将压缩包中的三个文件解压到同一目录（如 `D:\MHWS_Backup`）：
  - `CheckGameRunningWLog.exe`（主程序）
  - `TkinterGUI_zh_CN.exe`（配置工具）
  - `config.json`（配置文件）
- 确保目录路径不包含中文或特殊字符。

### 2. 配置工具使用
1. 双击运行 `TkinterGUI.exe`，打开图形界面。
2. 在界面中修改以下配置项：
   - **================一定要修改================**
   - **备份目录**：希望存档备份文件存储的目标路径（例:如填写`D:\\MHWS_Backup`，存档文件将备份在`D:\MHWS_Backup\202503141530`(当前日期、时间)文件夹中）。
   - **源存档目录**：游戏存档的原始路径,一般为`*Steam安装盘*D:\\Steam\\userdata\\*你的数字用户ID*\\2246340\\remote\\win64_save`。
   - **================可选修改================**
   - **备份间隔**：在检测到游戏启动后，隔多长时间进行一次备份（秒）。
   - **检查间隔**：检测游戏是否运行的间隔时间（秒）。
   - **最大日志行数**：日志文件的最大行数。
   - **最大备份数量**：保留的备份文件数量上限。
   - **日志文件名**：日志文件的名称，日志文件会默认生成于被解压的三个文件相同的目录。
   - **================如果只用来备份MHWS，不要修改================**
   - **检测启动的执行文件**：需要被检测启动的可执行文件名（默认为 `monsterhunterwilds.exe`，如需要备份其它游戏类型可以进行修改，文件名为根文件夹中可执行文件的名称，如`helldivers2.exe`、`WINWORD.EXE`）。
   - **文件匹配模式**：需要备份的文件模式（每行一个）|默认为MHWS的存档文件类型，可以按需求更改，如`要保存的word.docx`|`要保存的Excel.xls`|源存档目录下所有的txt文件`*.txt`。
3. 点击 **保存配置**，配置将保存到 `config.json`。

### 3. 配置任务计划程序
1. 打开 **任务计划程序**。
2. 创建基本任务：
   - 名称：`MHWS自动备份`（或任何其它名字，建议命好辩认的名字并添加描述）
   - 触发器：**当用户登录时**
   - 操作：**启动程序**
   - 启动程序：**程序或脚本：**选择文件夹中的CheckGameRunningWLog.exe文件，应该显示为如`D:\MHWS_Backup\CheckGameRunningWLog.exe`的格式，**起始于（可选）：**程序所在目录文件夹，如`D:\MHWS_Backup`。
   - 点击完成，右键点击刚刚添加的计划程序，选择**属性**
3. 属性：
   - 常规：勾选**使用最高权限运行**(如果不勾选该选项脚本也可以随正常用户登录启动运行，可以不勾选)。
   - 在 **设置** 中的 **如果此任务已经运行，以下规则适用** 选项选择 **请勿启动新实例**。

### 4. 测试任务计划
- 手动运行任务（双击CheckGameRunningWLog.exe），在任务管理器中确认程序是否正常启动。
- 重启电脑，在任务管理器中确认程序是否自动启动。

### 5. 终止程序（可选）
- 双击运行 `StopBackup.exe`，正在运行的程序会在 10 秒内关闭。

### 额外注意事项
- 请确保程序所在目录有写入权限。
- 如果程序未启动或未能正确备份文件，请检查文件夹内的 `backup_monitor.log` 日志文件。

---

## 文件说明
- `CheckGameRunningWLog.exe`：主程序，用于自动备份。
- `TkinterGUI.exe`：图形界面配置工具。
- `StopBackup.exe`：终止工具，用于关闭主程序。
- `config.json`：配置文件，存储所有配置项。

---

## 反馈与支持
这是我的第一个（正式传到github上）的项目，如有问题或建议还请联系我，任何合理的批评、建议和改进都会被积极采纳、慎重对待。无论如何都非常感谢 <3




## Features
- **Auto Backup**: Detects the game's running status and automatically backs up save files.
- **Graphical Configuration Interface**: Provides a graphical user interface (GUI) for easy modification of configuration files.
- **Logging**: Provides logging functionality to track whether the script starts and runs correctly.
- **Single Instance**: Ensures only one instance of the backup program runs at a time, avoiding redundant processes that consume system resources.

## Usage Instructions

### 1. Preparation
- Download the zip archive from the [release](https://github.com/acatsamaovo/AutoBackupForMHWS/releases/tag/v1.0.0).
- Extract the three files from the archive to the same directory (e.g., `D:\MHWS_Backup`):
  - `CheckGameRunningWLog.exe` (Main program)
  - `TkinterGUI_en_US.exe` (Configuration tool)
  - `config.json` (Configuration file)
- Ensure the directory path does not contain Chinese characters or special symbols.

### 2. Using the Configuration Tool
1. Double-click `TkinterGUI.exe` to open the GUI.
2. Modify the following settings in the interface:
   - **================ Must Modify ================**
   - **Backup Directory**: The target path where you want the backup files to be stored (e.g., if you enter `D:\\MHWS_Backup`, the backup files will be saved in a folder like `D:\MHWS_Backup\202503141530` (current date and time)).
   - **Source Directory**: The original path of the game save files, usually `*Steam installation drive*D:\\Steam\\userdata\\*your numeric user ID*\\2246340\\remote\\win64_save`.
   - **================ Optional Modifications ================**
   - **Backup Interval**: The time interval (in seconds) between backups after detecting the game is running.
   - **Check Interval**: The time interval (in seconds) for checking if the game is running.
   - **Max Log Lines**: The maximum number of lines in the log file.
   - **Max Backups**: The maximum number of backup files to retain.
   - **Log File Name**: The name of the log file, which will be generated in the same directory as the extracted files by default.
   - **================ Do Not Modify if Only Backing Up MHWS ================**
   - **Executable to Detect**: The name of the executable file to detect (default is `monsterhunterwilds.exe`; modify if backing up other games or programs, e.g., `helldivers2.exe`, `WINWORD.EXE`).
   - **File Patterns**: The file patterns to back up (one per line) | Default is MHWS save file types; can be modified as needed, e.g., `word.docx`, `Excel.xls`, or all txt files in the source directory `*.txt`.
3. Click **Save Configuration** to save the settings to `config.json`.

### 3. Configuring Task Scheduler
1. Open **Task Scheduler**.
2. Create a basic task:
   - Name: `MHWS Auto Backup` (or any other name; it is recommended to use a recognizable name and add a description).
   - Trigger: **When I log on**.
   - Action: **Start a program**.
   - Program/script: Select the `CheckGameRunningWLog.exe` file in the folder, which should display as `D:\MHWS_Backup\CheckGameRunningWLog.exe`.
   - Start in (optional): The directory where the program is located, e.g., `D:\MHWS_Backup`.
   - Click Finish, then right-click the newly created task and select **Properties**.
3. Properties:
   - General: Check **Run with highest privileges** (if this option is not checked, the script can still run when the user logs in normally, so it is optional).
   - Under **Settings**, for **If the task is already running, then the following rule applies**, select **Do not start a new instance**.

### 4. Testing the Task
- Manually run the task (double-click `CheckGameRunningWLog.exe`) and confirm in Task Manager that the program starts correctly.
- Restart your computer and confirm in Task Manager that the program starts automatically.

### 5. Stopping the Program (Optional)
- Double-click `StopBackup.exe`, and the program will close within 10 seconds.

### Additional Notes
- Ensure the program directory has write permissions.
- If the program fails to start, check the `backup_monitor.log` file for details.

---

## File Descriptions
- `CheckGameRunningWLog.exe`: The main program for auto backup.
- `TkinterGUI.exe`: The GUI configuration tool.
- `StopBackup.exe`: A tool to stop the main program.
- `config.json`: The configuration file storing all settings.

---

## Feedback & Support
This is my first (officially uploaded to github but also smol smol) project, please contact me if you have any questions or suggestions, any reasonable criticism, suggestions and improvements will be taken positively and with care.(Also apologies for translated potato English) Leave a star would be so much help if this helps you in someway, much love for all of you <3