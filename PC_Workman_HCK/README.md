#  PC_Workman_HCK  
**Part of the [HCK_Labs](https://github.com/HuckleR2003/HCK_Labs)** — modular system monitoring and AI-assisted diagnostics framework (demo).  

Version: **2.0.0 (Current — Diagnostic Expansion)**  
Author: **Marcin “HuckleR” Firmuga (HCK)**  
Status: *Beta — Fixing known issues (diagnostic refresh error)*

---

##  Overview
`PC_Workman_HCK` is an educational and diagnostic framework simulating real-time system monitoring.  
It’s designed as an **educational tool** for understanding modular Python architectures, GUI integration, and AI-assisted analytics.

This version introduces an expanded diagnostic engine, refined GUI, and improved modular registry — but currently contains a **known bug in the data refresh handler**.

---

##  Core Features
- **Dynamic Component Registry:** all modules auto-register via `import_core`.
- **Tkinter UI:** real-time demo interface showing CPU, GPU, RAM usage.
- **Stats Engine:** averages, trends, and log aggregation via CSV.
- **AI Placeholder:** ready for integration with `hck-GPT` (planned for v2.1.0).
- **Theme Engine:** consistent color scheme and modular UI elements.

---

##  Known Issue (v2.0.0)
 **Diagnostic Refresh Bug:**  
When multiple modules refresh simultaneously, the `avg_calculator` may crash due to file access conflict in `/data/logs/hourly_usage.csv`.  
Temporary workaround: run demo in single-threaded mode using `python startup.py --safe`.

---

##  Folder Structure
PC_Workman_HCK/
├── import_core.py
├── startup.py
├── setup.py
│
├── ui/
│ ├── main_window.py
│ ├── dialogs.py
│ ├── charts.py
│ ├── theme.py
│
├── hck_stats_engine/
│ ├── avg_calculator.py
│ ├── time_utils.py
│
├── data/logs/
│ └── hourly_usage.csv
└── README.md


---

 Roadmap
Version	Status	Description
v1.0.0	 Released	Initial architecture and GUI demo
v2.0.0	 Current	Added charting layer and extended stats, but has bug
v2.1.0	 Planned	Fix refresh crash, add GPU trend visualizations

Marcin “HuckleR” Firmuga — HCK_Labs
 AI Engineer & Security-Minded Developer
 LinkedIn -           https://www.linkedin.com/in/marcin-firmuga-a665471a3

 GitHub -             https://github.com/HuckleR2003

 firmuga.marcin.s@gmail.com