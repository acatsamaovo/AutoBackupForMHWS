import socket
import tkinter as tk
from tkinter import messagebox

def stop_backup():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 12357))
        s.send(b"exit")
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Backup Stopped", "Backup process has been stopped.")
        root.destroy()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Error", f"Failed to stop backup: {e}")
        root.destroy()

if __name__ == "__main__":
    stop_backup()