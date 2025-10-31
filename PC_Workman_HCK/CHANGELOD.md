### 🧾 `CHANGELOG.md`
# * HCK_Labs * — PC_Workman_HCK — Changelog
All notable changes are documented here.  
---

## [v2.0.0] — 2025-10-31
### Diagnostic Expansion — *Current (bug present)*
**Summary**
- Expanded diagnostic UI layout.
- Integrated new chart placeholders using matplotlib stubs.
- Added background scheduler for data refresh (bug source).
- Introduced GPU trend averaging.
- Enhanced theme colors and layout polish.

**Known Issue**
- Crash occurs during concurrent `avg_calculator` refresh events when multiple UI triggers overlap.

**Next Step**
- Patch under development (v2.0.1) — expected fix for thread-safe CSV read/write.

---

## [v1.0.0] — 2025-10-27
### Alpha Demo — “Diagnostics Foundation”
- Implemented registry system (`import_core`).
- Created Tkinter-based UI showing mock CPU/GPU/RAM usage.
- Added logging and average calculator modules.
- Packaged project with `setup.py`.
- Verified architecture for HCK_Labs integration.

---

### 📘 Notes
- Repository path: `/projects/PC_Workman_HCK/`
- Maintainer: **Marcin Firmuga**
- Scope: Educational diagnostics and monitoring tool.
