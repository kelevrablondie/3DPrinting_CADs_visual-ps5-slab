# Fit tests: print these first (2026-11-10)
Order and checks are in `TODO.md` → "Later: when you have a printer". Open the `.3mf` files in Bambu Studio.
1. `1_coupon_F11_small_corner.3mf`: stock-plate scan around clip F11 (from `analysis/coupon.py`). Tests the scan's hook fit.
2. `2_coupon_F5_large_spring.3mf`: same, clip F5.
3. `3_fit_strip_offcut.3mf`: built by `cad/fit_tests.py` from `cad/wrap.py`. Clip strip `disk_bottom` plus a disc-plate
   offcut with its dovetail rails, end stop and latch ledge, laid out flat on the bed. Tests the slide fit (0.2 mm) and the stop and latch.
Re-export after a design change: `cadgen +0.8.4 run cad/fit_tests.py`, then `cadgen export <id> deliverables/fit_tests/3_fit_strip_offcut.3mf`.
