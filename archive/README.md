# Archive: declined designs (moved 2026-11-10)
Kept for reference, not maintained; nothing in the live project imports these.
- `cad/concepts.py`, `concept_d.py`, `concept_e.py` + PNGs: rejected concepts A/B/C, enclosed D, open E.
- `cad/check_end_walls.py`, `analysis/end_edges.py`, `cad/renders/ends_*.png`: semi-open end walls (rejected 2026-11-02).
  Their code is still inside `cad/slab.py` (`END_FLAT`, `END_DISC`, `end_wall_cut`), which `wrap.py` imports.
- `analysis/frame.py`, `analysis/adapter_concept.png`, `deliverables/adapter_flat_concept.stl`: adapter-frame concept.
- `deliverables/ps5_clip_shelves_v2.zip`: glued clip shelves, replaced by slide-in clip strips (`cad/wrap.py`).
  The shelf meshes (`analysis/shelf_*.stl`, `cad/core/shelf_*_c.step`) stay live: the strips are cut from them.
