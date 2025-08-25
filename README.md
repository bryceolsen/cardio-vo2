# PROJECT-X — Energy Cost & Efficiency of Incline Treadmill vs StairMaster

Measure and compare the energy cost of **incline treadmill walking** and **StairMaster** using **Apple Watch “Active” kcal/min (measured by me)** and **ACSM metabolic equations**, then compute **mechanical power** and **mechanical efficiency** to guide training.

---

## TL;DR (Executive Summary)

- **Data:** Real Apple Watch *Active kcal/min* readings taken during treadmill and StairMaster sessions, logged to CSV. Multiple body masses included. StairMaster step height fixed at **0.2032 m**.
- **Theory:** ACSM walking & stepping equations → convert VO₂ to **kcal/min (gross)** → subtract rest (3.5 mL·kg⁻¹·min⁻¹) to get **NET** (comparable to AW Active).
- **Power & Efficiency:**  
  - Mechanical power: treadmill \(P_\mathrm{mech}=m g v \cdot \mathrm{grade}\), stairs \(P_\mathrm{mech}=m g h \cdot (\mathrm{SPM}/60)\).  
  - Metabolic power \(P_\mathrm{met}\) from kcal/min (1 kcal·min⁻¹ ≈ 69.78 W).  
  - **Efficiency** \( \eta = P_\mathrm{mech}/P_\mathrm{met} \).
- **Findings:**  
  1) **StairMaster (theory)** efficiency is ~constant **≈ 0.138 (13.8%)** when step height is fixed (mass & SPM cancel in the ratio).  
  2) **Treadmill** efficiency varies by condition (≈ **0.10–0.25** here) and generally **increases with speed & grade**.  
  3) **Mass-invariant efficiency:** for a fixed condition, η is ~unchanged across masses (both numerator/denominator scale with mass).  
  4) At **0% grade** the vertical mechanical work is ~0 → **vertical efficiency is N/A (shows as 0)** even though metabolic cost is positive.

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

**ACSM treadmill (walking)**  
- \( S = \text{speed}_{\text{mph}} \times 26.8224\ \mathrm{m·min^{-1}} \), \( G = \text{grade} / 100 \)  
- \( \mathrm{VO}_2^\text{gross} = 3.5 + 0.1S + 1.8SG \) (mL·kg⁻¹·min⁻¹)

**ACSM stepping (stairs)**  
- \( \mathrm{VO}_2^\text{gross} = 3.5 + 0.2\cdot \mathrm{SPM} + 2.4\cdot \mathrm{SPM}\cdot h \)

**Convert to NET & power**  
- \( \mathrm{VO}_2^\text{net} = \mathrm{VO}_2^\text{gross} - 3.5 \)  
- \( \text{kcal/min} = \mathrm{VO}_2(\mathrm{L/min}) \times 5 \) where \( \mathrm{VO}_2(\mathrm{L/min}) = \mathrm{VO}_2(\mathrm{mL·kg^{-1}·min^{-1}}) \times \frac{m_{\text{kg}}}{1000} \)  
- \( P_\mathrm{met} = \text{kcal/min} \times 69.78\ \mathrm{W} \)  
- Treadmill \( P_\mathrm{mech}=m g v G \) ; Stair \( P_\mathrm{mech}=m g h (\mathrm{SPM}/60) \)  
- Efficiency \( \eta = P_\mathrm{mech}/P_\mathrm{met} \). For level walking (0% grade), \(P_\mathrm{mech}\approx 0\) → η is effectively N/A.

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

## Applications

- **Fat-loss (max kcal/min):** choose conditions with higher **NET kcal/min** (steeper grades / higher SPM) at a safe RPE. Efficiency is diagnostic but not the target.
- **Economy / rehab:** for a given vertical power, pick **higher-efficiency** settings (often moderate treadmill grade at steady speed, or StairMaster with SPM tuned to your target). Lower metabolic cost → longer sustainable efforts.
- **Hiking prep:** match target **vertical speed** (treadmill \(v\cdot G\), stair \( \mathrm{SPM}\cdot h / 60 \)); progress time at target before increasing the target.
- **Device calibration mindset:** if your Apple Watch consistently over/underestimates for a condition, you can apply a personal correction factor in analysis (optional).

---

## Limitations

Wearable algorithm variance, handrail use, footwear/surface, and individual biomechanics. At 0% grade, vertical efficiency isn’t meaningful (mechanical power ≈ 0).

---

## License

MIT (or your choice).
