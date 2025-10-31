"""core.monitor
Simple, mockable monitor for CPU/GPU/RAM usage.
In production replace mocks with psutil and GPU libs (pynvml/wmi).
"""
from import_core import register_component
import time, random

class Monitor:
    """Mock Monitor class. Use `read()` to get current usage snapshot."""
    def __init__(self):
        self.name = "Monitor"
        register_component('core.monitor', self)

    def read(self):
        # Mock data: replace with psutil in production
        snapshot = {
            'timestamp': int(time.time()),
            'cpu_percent': round(random.uniform(1, 95), 2),
            'gpu_percent': round(random.uniform(0, 90), 2),
            'ram_percent': round(random.uniform(5, 95), 2),
            'processes': [
                {'pid': 1001, 'name': 'GTA5.exe', 'cpu': round(random.uniform(0,30),2), 'ram': round(random.uniform(0,10),2)},
                {'pid': 2002, 'name': 'chrome.exe', 'cpu': round(random.uniform(0,25),2), 'ram': round(random.uniform(1,15),2)},
            ]
        }
        return snapshot

# convenience instance
monitor = Monitor()
