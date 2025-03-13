import logging
from logging.handlers import RotatingFileHandler
import time
import psutil
import os
import glob
from datetime import datetime
import shutil
import os, json


config_file = os.path.join(os.path.dirname(__file__), 'config.json')
if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    raise FileNotFoundError("配置文件 config.json 未找到，请先创建配置文件。")

backup_dir = config.get("backup_dir", r"D:\\BackUp\\MHWS")
src_dir = config.get("src_dir", r"E:\\Steam\\userdata\\1218322048\\2246340\\remote\\win64_save")
log_file = os.path.join(os.path.dirname(__file__), config.get("log_file", "backup_monitor.log"))
backup_interval = config.get("backup_interval", 600)
check_interval = config.get("check_interval", 10)
MAX_LOG_LINES = config.get("MAX_LOG_LINES", 100)
MAX_BACKUPS = config.get("MAX_BACKUPS", 20)
game_executable = config.get("game_executable", "monsterhunterwilds.exe")



# 日志记录器相关配置
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

def backup_files():


    logger.info("===================================================================\n")
    

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    dest_dir = os.path.join(backup_dir, timestamp)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        logger.info(f"创建目录: {dest_dir}")
    
    # 定义需要匹配的文件模式（可应对文件名中数字的变化）
    patterns = ["data00-*.bin", "data00*Slot.bin"]
    files_copied = []
    
    for pattern in patterns:
        search_pattern = os.path.join(src_dir, pattern)
        logger.info(f"搜索路径: {search_pattern}")
        for file_path in glob.glob(search_pattern):
            file_name = os.path.basename(file_path)
            dest_file_path = os.path.join(dest_dir, file_name)
            try:
                shutil.copy2(file_path, dest_file_path)
                files_copied.append(file_name)
                logger.info(f"成功复制文件: {file_name}")
            except Exception as e:
                print(f"复制文件 {file_name} 失败: {e}")
                logger.info(f"复制文件 {file_name} 失败: {e}")
    
    if files_copied:
        print("备份成功，复制的文件：", files_copied)
        logger.info(f"备份成功，复制的文件：{files_copied}")
    else:
        print("未找到匹配的文件。")
        logger.info("未找到匹配的文件。")

def trim_log_file():
    """保持日志文件最大行数，避免日志无限增长"""

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if len(lines) > MAX_LOG_LINES:
            with open(log_file, "w", encoding="utf-8") as f:
                f.writelines(lines[-MAX_LOG_LINES:])  # 只保留最新的 MAX_LOG_LINES 行

def clean_old_backups():
    """删除旧的备份，确保只保留最新的 MAX_BACKUPS 份"""

    backups = sorted(glob.glob(os.path.join(backup_dir, "*")), key=os.path.getmtime)

    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[:-MAX_BACKUPS]:  # 仅删除超出的旧备份
            try:
                if os.path.isdir(old_backup):
                    shutil.rmtree(old_backup)  # 删除空文件夹
                else:
                    os.remove(old_backup)  # 删除文件
                logger.info(f"已删除过旧备份: {old_backup}")
            except Exception as e:
                logger.info(f"删除备份失败: {old_backup}，错误: {e}")

def main():

    logger.info("监控脚本启动，等待检测游戏进程...")
    while True:
        if is_game_running():
            logger.info("检测到游戏正在运行，开始执行备份任务。")
            backup_files()
            logger.info("备份任务启用成功")
            trim_log_file()
            clean_old_backups()
            logger.info("冗余日志与备份清理完成")
            logger.info(f"备份任务完成，等待 {backup_interval} 秒后再次备份。")
            time.sleep(backup_interval)
        else:
            logger.info("游戏未运行，继续等待...")
            time.sleep(check_interval)

if __name__ == "__main__":
    main()
