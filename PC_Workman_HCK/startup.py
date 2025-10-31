"""startup.py
Entry point for PC Workman skeleton. Initializes components and runs a demo UI.
"""
from import_core import COMPONENTS
# import to register components
import core.monitor, core.logger, core.analyzer, core.scheduler
import ai.hck_gpt, ai.ai_logic, ai.detector
import hck_stats_engine.avg_calculator, hck_stats_engine.trend_analysis
import ui.main_window

def run_demo():
    print('Starting PC Workman demo (skeleton)...')
    # start scheduler loop in background
    try:
        COMPONENTS.get('core.scheduler').start_loop()
    except Exception:
        pass
    # UI demo
    ui = ui.main_window.MainWindow()
    ui.run()

if __name__ == '__main__':
    run_demo()
