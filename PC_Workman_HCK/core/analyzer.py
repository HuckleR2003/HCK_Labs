"""core.analyzer
Simple analyzer for detecting spikes and suspicious patterns.
"""
from import_core import register_component
import statistics, time

class Analyzer:
    def __init__(self):
        register_component('core.analyzer', self)

    def average(self, values):
        if not values:
            return 0
        return round(statistics.mean(values), 2)

    def detect_spike(self, series, threshold_percent=30):
        # naive spike detection: compare last value to mean of previous values
        if len(series) < 2:
            return False, None
        last = series[-1]
        prev_mean = statistics.mean(series[:-1]) if len(series) > 1 else series[0]
        if prev_mean == 0:
            return False, None
        diff = ((last - prev_mean) / prev_mean) * 100
        return abs(diff) >= threshold_percent, round(diff, 2)

analyzer = Analyzer()
