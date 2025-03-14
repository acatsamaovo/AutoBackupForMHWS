import logging
from logging.handlers import RotatingFileHandler
import time
import psutil
import os
import glob
from datetime import datetime
import shutil
import os, json
import sys
import socket
import threading
import tkinter as tk
from tkinter import messagebox


config_file = os.path.join(os.path.dirname(sys.executable), 'config.json')
if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    raise FileNotFoundError("Configuration file config.json is not found, please create the configuration file first.")


# Configuration
exe_dir = os.path.dirname(sys.executable)
log_file = os.path.join(exe_dir, config.get("log_file", "backup_monitor.log"))
backup_dir = config.get("backup_dir", r"D:\\BackUp\\MHWS")
src_dir = config.get("src_dir", r"E:\\Steam\\userdata\\1218322048\\2246340\\remote\\win64_save")
backup_interval = config.get("backup_interval", 600)
check_interval = config.get("check_interval", 10)
MAX_LOG_LINES = config.get("MAX_LOG_LINES", 100)
MAX_BACKUPS = config.get("MAX_BACKUPS", 20)
game_executable = config.get("game_executable", "monsterhunterwilds.exe").lower()
patterns = ["data00-*.bin", "data00*Slot.bin"]


# Logger related configuration
logger = logging.getLogger("BackupMonitor")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



def is_game_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == game_executable:
            return True
    return False

def show_message(title, message):
    root = tk.Tk()
    root.withdraw()
    root.after(3000, lambda: root.destroy())
    messagebox.showinfo(title, message)
    root.mainloop()

def is_already_running():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 12357))
        return False
    except socket.error:
        show_message("Warning", "The program is already running, please do not start it again!")
        return True
    finally:
        s.close()

def backup_files():
    logger.info("===================================================================\n")
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    dest_dir = os.path.join(backup_dir, timestamp)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        logger.info(f"Created directory: {dest_dir}")
    
    files_copied = []
    
    for pattern in patterns:
        search_pattern = os.path.join(src_dir, pattern)
        logger.info(f"Search path: {search_pattern}")
        for file_path in glob.glob(search_pattern):
            file_name = os.path.basename(file_path)
            dest_file_path = os.path.join(dest_dir, file_name)
            try:
                shutil.copy2(file_path, dest_file_path)
                files_copied.append(file_name)
                logger.info(f"Successfully copied file: {file_name}")
            except Exception as e:
                print(f"Failed to copy file {file_name}: {e}")
                logger.info(f"Failed to copy file {file_name}: {e}")
    
    if files_copied:
        print("Backup successful, copied files: ", files_copied)
        logger.info(f"Backup successful, copied files: {files_copied}")
    else:
        print("No matching files found.")
        logger.info("No matching files found.")

def trim_log_file():

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if len(lines) > MAX_LOG_LINES:
            with open(log_file, "w", encoding="utf-8") as f:
                f.writelines(lines[-MAX_LOG_LINES:])  

def clean_old_backups():

    backups = sorted(glob.glob(os.path.join(backup_dir, "*")), key=os.path.getmtime)

    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[:-MAX_BACKUPS]: 
            try:
                if os.path.isdir(old_backup):
                    shutil.rmtree(old_backup)  
                else:
                    os.remove(old_backup)  
                logger.info(f"Deleted old backup: {old_backup}")
            except Exception as e:
                logger.info(f"Failed to delete backup: {old_backup}, error: {e}")

def exit_listener():
    exit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    exit_socket.bind(('127.0.0.1', 12357))
    exit_socket.listen(1)
    while True:
        conn, _ = exit_socket.accept()
        conn.recv(1024)
        logger.info("Exit signal received, program being terminated...")
        os._exit(0)

def main():

    logger.info("Monitoring script started, waiting to detect game process...")
    threading.Thread(target=exit_listener, daemon=True).start()
    while True:
        if is_game_running():
            logger.info("Game detected running, starting backup task.")
            backup_files()
            logger.info("Backup task successfully started.")
            trim_log_file()
            clean_old_backups()
            logger.info("Redundant logs and backups cleaned up.")
            logger.info(f"Backup task completed, waiting {backup_interval} seconds before next backup.")
            time.sleep(backup_interval)
        else:
            logger.info("Game not running, continuing to wait...")
            time.sleep(check_interval)

if __name__ == "__main__":
    if is_already_running():
        sys.exit(1)
    else:
        main()
