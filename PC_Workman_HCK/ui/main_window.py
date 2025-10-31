"""ui.main_window
Very small demo UI using Tkinter to show mock stats.
"""
from import_core import COMPONENTS
import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('PC Workman - HCK_Labs (Demo)')
        self.label = ttk.Label(self.root, text='PC Workman – demo UI (mock data)')
        self.label.pack(padx=10, pady=10)
        self.stats_box = tk.Text(self.root, height=10, width=60)
        self.stats_box.pack(padx=10, pady=10)
        self.refresh_button = ttk.Button(self.root, text='Refresh', command=self.refresh)
        self.refresh_button.pack(padx=10, pady=(0,10))

    def refresh(self):
        monitor = COMPONENTS.get('core.monitor')
        snapshot = monitor.read() if monitor else {'cpu_percent':0,'gpu_percent':0,'ram_percent':0}
        self.stats_box.delete('1.0','end')
        self.stats_box.insert('end', f"CPU: {snapshot['cpu_percent']}%\nGPU: {snapshot['gpu_percent']}%\nRAM: {snapshot['ram_percent']}%\n")

    def run(self):
        self.refresh()
        self.root.mainloop()

if __name__ == '__main__':
    MainWindow().run()
