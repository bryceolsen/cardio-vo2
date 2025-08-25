# CARDIO VO2 — Energy Cost & Efficiency of Incline Treadmill vs StairMaster

Measure and compare the energy cost of **incline treadmill walking** and **StairMaster** using **Apple Watch “Active” kcal/min (measured by me)** and **ACSM metabolic equations**, then compute **mechanical power** and **mechanical efficiency** to guide training.

---

## TL;DR (Executive Summary)

- **Data:** Real Apple Watch *Active kcal/min* recorded on treadmill + StairMaster; multiple body masses; Stair step height fixed at **0.2032 m**.  
- **Theory:** ACSM walking & stepping → VO₂ (gross) → subtract resting 3.5 to get **NET** kcal/min (comparable to AW Active).  
- **Efficiency:**  
  - **StairMaster (theory)** is ~constant **≈ 0.138 (13.8%)** at fixed step height (mass & SPM cancel in the ratio).  
  - **Treadmill** efficiency varies by condition (≈ **0.10–0.25** here) and generally increases with **speed & grade**. At **0% grade**, vertical mechanical work ≈ 0 → vertical efficiency is effectively **N/A (0)** even though metabolic cost is > 0.  
- **Mass effect:** For a fixed condition, η is ~mass-invariant (both mech & met powers scale ~linearly with mass).

---

## Repository Layout

```
project-x/
├─ README.md
├─ requirements.txt
├─ data/                # CSV with measured Apple Watch data
├─ figures/             # Saved plots (PNG/SVG/PDF)
├─ exports/             # Final HTML/PDF report
└─ notebooks/           # Jupyter notebook (optional)
```

- Primary dataset: `data/apple_watch_data.csv` (your measured trials)
- Report (exported from notebook): `exports/PROJECT-X.html`
- Example figures:
  - `figures/fig_treadmill_efficiency_vs_grade.png`
  - `figures/fig_stair_aw_vs_acsm.png`

---

## Methods (brief)

### Notation (units)
- `S` = treadmill speed in **m/min** = `mph × 26.8224`
- `G` = grade as **fraction** = `grade_percent / 100`
- `v` = treadmill speed in **m/s** = `mph × 0.44704`
- `h` = step height in **m** (StairMaster) = `0.2032`
- `m` = body mass in **kg`
- `g` = 9.80665 **m/s²** (gravity)

### ACSM treadmill (walking)
VO2_gross (mL·kg⁻¹·min⁻¹) = 3.5 + 0.1·S + 1.8·S·G

### ACSM stepping (stairs)
VO2_gross (mL·kg⁻¹·min⁻¹) = 3.5 + 0.2·SPM + 2.4·SPM·h

### Convert VO₂ to kcal/min (NET)
VO2_net (mL·kg⁻¹·min⁻¹) = VO2_gross − 3.5
kcal/min = (VO2_net / 1000) · m · 5

### Powers
Metabolic power: P_met (W) = (kcal/min) × 69.78
Treadmill mechanical: P_mech (W) = m · g · v · G
Stair mechanical: P_mech (W) = m · g · h · (SPM / 60)

### Efficiency (vertical)
η = P_mech / P_met

---

## How to Reproduce

```bash
# 1) Install Python deps
pip install -r requirements.txt

# 2) Open the notebook
jupyter notebook  # or jupyter lab

# 3) Run cells
# Ensure data paths point to files in /data/
```

**Saving figures (inside the notebook):**
```python
from pathlib import Path
Path("figures").mkdir(exist_ok=True)
fig.savefig("figures/fig_treadmill_efficiency_vs_grade.png", dpi=300, bbox_inches="tight")
```

---

## Findings (efficiency)

1. **StairMaster (theory)** ≈ **0.138** constant at step height **0.2032 m** (mass & SPM cancel).  
2. **Treadmill** η varies by condition (≈ **0.10–0.25** here) and rises with **speed & grade**; at 0% grade, vertical η is **N/A (0)**.  
3. **Mass-invariant η** per condition (both numerator & denominator scale ~linearly with mass).  
4. **Mode choice by goal:**  
   - **Economy/rehab/hiking:** pick **higher-efficiency** settings for the same vertical power (lower kcal/min).  
   - **Fat-loss:** prioritize **kcal/min** (steeper grade / higher SPM at safe RPE).

---

## Applications

- **Fat-loss (max kcal/min):** choose conditions with higher **NET kcal/min** (steeper grades / higher SPM) at a safe RPE. Efficiency is diagnostic but not the target.  
- **Economy / rehab:** for a given vertical power, pick **higher-efficiency** settings (often moderate treadmill grade at steady speed, or StairMaster with SPM tuned to your target). Lower metabolic cost → longer sustainable efforts.  
- **Hiking prep:** match target **vertical speed** (treadmill `v·G`, stair `SPM·h/60`); progress time at target before increasing the target.  
- **Device calibration mindset (optional):** if your Apple Watch consistently over/underestimates for a condition, note a personal correction factor in your analysis.

**Economy example (numbers rounded):** hold **150 W** vertical work.
- If `η = 0.14` → `P_met ≈ 150/0.14 = 1070 W` → **15.3 kcal/min**  
- If `η = 0.20` → `P_met ≈ 150/0.20 = 750 W`  → **10.8 kcal/min**  
Same vertical work, ~**30% fewer kcal/min** at the more efficient setting.

---

## Limitations

Wearable algorithm variance, handrail use, footwear/surface, and individual biomechanics. At 0% grade, vertical efficiency isn’t meaningful (mechanical power ≈ 0).

---

## License

MIT (or your choice).
