import tkinter as tk
from tkinter import filedialog, messagebox
import json, os
import sys

def load_config():
    exe_dir = os.path.dirname(sys.executable)
    config_file = os.path.join(exe_dir, 'config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

def save_config(config):
    exe_dir = os.path.dirname(sys.executable)
    config_file = os.path.join(exe_dir, 'config.json')
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def browse_directory(entry):
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def create_gui():
    config = load_config()
    
    root = tk.Tk()
    root.title("备份脚本配置")

    # 备份目录
    tk.Label(root, text="备份目录:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    backup_dir_entry = tk.Entry(root, width=50)
    backup_dir_entry.grid(row=0, column=1, padx=5, pady=5)
    backup_dir_entry.insert(0, config.get("backup_dir", ""))
    tk.Button(root, text="浏览", command=lambda: browse_directory(backup_dir_entry)).grid(row=0, column=2, padx=5, pady=5)

    # 源存档目录
    tk.Label(root, text="源存档目录:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    src_dir_entry = tk.Entry(root, width=50)
    src_dir_entry.grid(row=1, column=1, padx=5, pady=5)
    src_dir_entry.insert(0, config.get("src_dir", ""))
    tk.Button(root, text="浏览", command=lambda: browse_directory(src_dir_entry)).grid(row=1, column=2, padx=5, pady=5)

    # 备份间隔
    tk.Label(root, text="备份间隔 (秒):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    backup_interval_entry = tk.Entry(root)
    backup_interval_entry.grid(row=2, column=1, padx=5, pady=5)
    backup_interval_entry.insert(0, config.get("backup_interval", 600))

    # 检查间隔
    tk.Label(root, text="检查间隔 (秒):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    check_interval_entry = tk.Entry(root)
    check_interval_entry.grid(row=3, column=1, padx=5, pady=5)
    check_interval_entry.insert(0, config.get("check_interval", 10))

    def save_and_exit():
        try:
            new_config = {
                "backup_dir": backup_dir_entry.get(),
                "src_dir": src_dir_entry.get(),
                "backup_interval": int(backup_interval_entry.get()),
                "check_interval": int(check_interval_entry.get())
            }
        except ValueError:
            messagebox.showerror("输入错误", "请确保备份间隔和检查间隔为数字。")
            return
        save_config(new_config)
        messagebox.showinfo("配置保存", "配置已保存！")
        root.destroy()

    tk.Button(root, text="保存配置", command=save_and_exit).grid(row=4, column=1, pady=10)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
