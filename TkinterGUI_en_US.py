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
    root.title("Configuration Editor")

    tk.Label(root, text="Backup Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    backup_dir_entry = tk.Entry(root, width=50)
    backup_dir_entry.grid(row=0, column=1, padx=5, pady=5)
    backup_dir_entry.insert(0, config.get("backup_dir", ""))
    tk.Button(root, text="Browse", command=lambda: browse_directory(backup_dir_entry)).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Source Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    src_dir_entry = tk.Entry(root, width=50)
    src_dir_entry.grid(row=1, column=1, padx=5, pady=5)
    src_dir_entry.insert(0, config.get("src_dir", ""))
    tk.Button(root, text="Browse", command=lambda: browse_directory(src_dir_entry)).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(root, text="Backup Interval (seconds):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    backup_interval_entry = tk.Entry(root)
    backup_interval_entry.grid(row=2, column=1, padx=5, pady=5)
    backup_interval_entry.insert(0, config.get("backup_interval", 600))

    tk.Label(root, text="Check Interval (seconds):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    check_interval_entry = tk.Entry(root)
    check_interval_entry.grid(row=3, column=1, padx=5, pady=5)
    check_interval_entry.insert(0, config.get("check_interval", 10))

    tk.Label(root, text="Max Log Lines:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    max_log_lines_entry = tk.Entry(root)
    max_log_lines_entry.grid(row=4, column=1, padx=5, pady=5)
    max_log_lines_entry.insert(0, config.get("MAX_LOG_LINES", 100))

    tk.Label(root, text="Max Backups:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
    max_backups_entry = tk.Entry(root)
    max_backups_entry.grid(row=5, column=1, padx=5, pady=5)
    max_backups_entry.insert(0, config.get("MAX_BACKUPS", 20))

    tk.Label(root, text="Game Executable:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
    game_executable_entry = tk.Entry(root)
    game_executable_entry.grid(row=6, column=1, padx=5, pady=5)
    game_executable_entry.insert(0, config.get("game_executable", "monsterhunterwilds.exe"))

    tk.Label(root, text="Log File Name:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
    log_file_entry = tk.Entry(root)
    log_file_entry.grid(row=7, column=1, padx=5, pady=5)
    log_file_entry.insert(0, config.get("log_file", "backup_monitor.log"))

    tk.Label(root, text="File Patterns (one per line):").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
    patterns_text = tk.Text(root, height=4, width=40)
    patterns_text.grid(row=8, column=1, padx=5, pady=5)
    patterns_text.insert(tk.END, "\n".join(config.get("patterns", ["data00-*.bin", "data00*Slot.bin"])))

    def save_and_exit():
        try:
            new_config = {
                "backup_dir": backup_dir_entry.get(),
                "src_dir": src_dir_entry.get(),
                "backup_interval": int(backup_interval_entry.get()),
                "check_interval": int(check_interval_entry.get()),
                "MAX_LOG_LINES": int(max_log_lines_entry.get()),
                "MAX_BACKUPS": int(max_backups_entry.get()),
                "game_executable": game_executable_entry.get(),
                "log_file": log_file_entry.get(),
                "patterns": patterns_text.get("1.0", tk.END).strip().split("\n")
            }
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure numeric fields contain valid numbers.")
            return
        save_config(new_config)
        messagebox.showinfo("Success", "Configuration saved!")
        root.destroy()

    tk.Button(root, text="Save Configuration", command=save_and_exit).grid(row=9, column=1, pady=10)
    root.mainloop()
    
if __name__ == "__main__":
    create_gui()
