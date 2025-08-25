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

