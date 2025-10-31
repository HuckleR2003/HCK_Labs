"""core.scheduler
Simple scheduler that triggers hourly writes. In production use APScheduler or system scheduler.
"""
import time, threading
from import_core import register_component, COMPONENTS

class Scheduler:
    def __init__(self, interval_seconds=3600):
        self.interval = interval_seconds
        self._stop = False
        register_component('core.scheduler', self)

    def start_loop(self):
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()
        return t

    def _loop(self):
        while not self._stop:
            # In a real run you'd collect from monitor and call logger.write_hourly
            time.sleep(self.interval)

    def stop(self):
        self._stop = True

scheduler = Scheduler(interval_seconds=3600)
