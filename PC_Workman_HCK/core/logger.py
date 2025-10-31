"""core.logger
Writes hourly snapshots and aggregation helpers.
"""
from import_core import COMPONENTS, register_component
import os, csv, time, json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'logs')
os.makedirs(DATA_DIR, exist_ok=True)

HOURLY_CSV = os.path.join(DATA_DIR, 'hourly_usage.csv')

HEADER = ['timestamp', 'iso_time', 'cpu_percent', 'gpu_percent', 'ram_percent']

class Logger:
    def __init__(self):
        register_component('core.logger', self)
        # ensure file exists with header
        if not os.path.exists(HOURLY_CSV):
            with open(HOURLY_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(HEADER)

    def write_hourly(self, snapshot):
        iso = datetime.utcfromtimestamp(snapshot['timestamp']).isoformat()
        row = [snapshot['timestamp'], iso, snapshot['cpu_percent'], snapshot['gpu_percent'], snapshot['ram_percent']]
        with open(HOURLY_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def read_hourly(self):
        if not os.path.exists(HOURLY_CSV):
            return []
        with open(HOURLY_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

logger = Logger()
