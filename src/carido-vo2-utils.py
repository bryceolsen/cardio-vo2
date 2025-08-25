
"""
projectx_utils.py — Helpers for PROJECT-X

Functions included:
- ACSM equations (treadmill & stair), kcal/min conversions
- Mechanical & metabolic power, efficiency
- Data cleaning: remove_flat_treadmill
- Plotting: treadmill_efficiency_plot, stair_efficiency_plot
- Simple style_table for pretty DataFrames

Usage:
    from projectx_utils import (
        vo2_treadmill_gross_mLkgmin, vo2_stair_gross_mLkgmin,
        net_kcal_per_min_from_gross_vo2, kcal_per_min_from_vo2_mLkgmin,
        mech_power_treadmill_W, mech_power_stair_W, met_power_W, efficiency,
        remove_flat_treadmill, treadmill_efficiency_plot, stair_efficiency_plot,
        style_table
    )
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- ACSM equations & kcal/min --------------------

def vo2_treadmill_gross_mLkgmin(speed_mph, grade_pct):
    """ACSM walking gross VO2 (mL·kg⁻¹·min⁻¹).
    S = speed_mph * 26.8224 (m·min⁻¹), G = grade_pct/100 (fraction).
    """
    S = np.asarray(speed_mph, dtype=float) * 26.8224
    G = np.asarray(grade_pct, dtype=float) / 100.0
    return 3.5 + 0.1*S + 1.8*S*G

def vo2_stair_gross_mLkgmin(spm, step_h_m):
    """ACSM stepping gross VO2 (mL·kg⁻¹·min⁻¹)."""
    spm = np.asarray(spm, dtype=float)
    step_h_m = np.asarray(step_h_m, dtype=float)
    return 3.5 + 0.2*spm + 2.4*spm*step_h_m

def kcal_per_min_from_vo2_mLkgmin(vo2_mLkgmin, mass_kg):
    """Convert VO2 (mL·kg⁻¹·min⁻¹) to kcal/min for given mass (kg)."""
    vo2_L_min = (np.asarray(vo2_mLkgmin, dtype=float) * np.asarray(mass_kg, dtype=float)) / 1000.0
    return vo2_L_min * 5.0

def net_kcal_per_min_from_gross_vo2(vo2_gross_mLkgmin, mass_kg):
    """NET kcal/min by subtracting resting 3.5 mL·kg⁻¹·min⁻¹ from gross VO2."""
    return kcal_per_min_from_vo2_mLkgmin(np.asarray(vo2_gross_mLkgmin, dtype=float) - 3.5, mass_kg)

# -------------------- Mechanical & metabolic power, efficiency --------------------

def mech_power_treadmill_W(mass_kg, speed_mph, grade_pct, g=9.80665):
    """Vertical mechanical power on treadmill in Watts: m*g*v*grade."""
    v = np.asarray(speed_mph, dtype=float) * 0.44704  # mph -> m/s
    G = np.asarray(grade_pct, dtype=float) / 100.0
    return np.asarray(mass_kg, dtype=float) * g * v * G

def mech_power_stair_W(mass_kg, spm, step_h_m, g=9.80665):
    """Mechanical power on stairs in Watts: m*g*step_height*(spm/60)."""
    return np.asarray(mass_kg, dtype=float) * g * np.asarray(step_h_m, dtype=float) * (np.asarray(spm, dtype=float) / 60.0)

def met_power_W(kcal_per_min):
    """Metabolic power in Watts (1 kcal/min ≈ 69.78 W)."""
    return np.asarray(kcal_per_min, dtype=float) * 69.78

def efficiency(mech_W, met_W):
    """Return mech/met; np.nan where met_W<=0."""
    mech = np.asarray(mech_W, dtype=float)
    met = np.asarray(met_W, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        eta = mech / met
        eta[~np.isfinite(eta)] = np.nan
    return eta

# -------------------- Data cleaning --------------------

def remove_flat_treadmill(df: pd.DataFrame, tol_pct: float = 0.0) -> pd.DataFrame:
    """
    Drop rows where modality == 'treadmill' and grade_pct is within ±tol_pct of 0.
    """
    if df is None or df.empty:
        return df
    out = df.copy()
    out["modality_norm"] = out["modality"].astype(str).strip().str.lower()
    out["grade_num"] = pd.to_numeric(out.get("grade_pct"), errors="coerce")
    drop_mask = (out["modality_norm"] == "treadmill") & (out["grade_num"].abs() <= tol_pct)
    out = out.loc[~drop_mask].drop(columns=["modality_norm", "grade_num"])
    return out.reset_index(drop=True)

# -------------------- Plotting --------------------

def treadmill_efficiency_plot(treadmill_df: pd.DataFrame, save_to: Path | str = "figures/fig_treadmill_efficiency_vs_grade.png"):
    """
    Plot measured efficiency vs grade (lines by speed), overlay ACSM theory if present.
    Expects columns:
      - speed_mph, grade_pct
      - eff_measured or efficiency_measured
      - eff_theory_net or efficiency_theory_net
    Saves PNG to 'save_to' and returns the summarized DataFrame.
    """
    df = treadmill_df.copy()

    # column picks
    def pick(*names):
        for n in names:
            if n in df.columns: return n
        return None

    speed, grade = "speed_mph", "grade_pct"
    eff_meas = pick("eff_measured", "efficiency_measured")
    eff_theo = pick("eff_theory_net", "efficiency_theory_net")

    # coerce numerics if present
    for c in [speed, grade, eff_meas, eff_theo]:
        if c and c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # summarize
    need = [speed, grade] + ([eff_meas] if eff_meas else [])
    g = df.dropna(subset=[c for c in need if c]).groupby([speed, grade], as_index=False)
    agg = {"n": (speed, "count")}
    if eff_meas: agg["eff_meas"] = (eff_meas, "mean")
    if eff_theo: agg["eff_theory"] = (eff_theo, "mean")
    sumdf = g.agg(**agg).sort_values([speed, grade])

    # plot
    fig, ax = plt.subplots(figsize=(8, 5))
    if "eff_meas" in sumdf.columns:
        for spd, grp in sumdf.groupby(speed):
            ax.plot(grp[grade], grp["eff_meas"], marker="o", label=f"{spd:.0f} mph — measured")
    if "eff_theory" in sumdf.columns:
        for spd, grp in sumdf.groupby(speed):
            ax.plot(grp[grade], grp["eff_theory"], marker="s", linestyle="--", label=f"{spd:.0f} mph — ACSM theory")

    ax.set_xlabel("Grade (%)")
    ax.set_ylabel("Efficiency (mech/met)")
    ax.set_title("Treadmill: Efficiency vs Grade")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Speed")

    save_to = Path(save_to)
    save_to.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(save_to, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

    return sumdf

def stair_efficiency_plot(stair_df: pd.DataFrame, save_to: Path | str = "figures/fig_stair_aw_vs_acsm.png"):
    """
    Plot Apple Watch Active kcal/min vs ACSM NET across SPM.
    Expects columns: spm, aw_active_kcal_min, theory_net_kcal_min, and (optionally) efficiency_theory_net/eff_theory_net.
    """
    sta = stair_df.copy()
    for c in ["spm","aw_active_kcal_min","theory_net_kcal_min","efficiency_measured","efficiency_theory_net","eff_measured","eff_theory_net"]:
        if c in sta.columns:
            sta[c] = pd.to_numeric(sta[c], errors="coerce")

    # pick correct theory efficiency column if present
    eff_theory_col = "efficiency_theory_net" if "efficiency_theory_net" in sta.columns else ("eff_theory_net" if "eff_theory_net" in sta.columns else None)

    sta_sum = (
        sta.dropna(subset=["spm"])
           .groupby("spm", as_index=False)
           .agg(aw=("aw_active_kcal_min","mean"),
                net=("theory_net_kcal_min","mean"),
                efficiency_theory=(eff_theory_col,"mean") if eff_theory_col else ("spm","count"))
           .sort_values("spm")
    )

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(sta_sum["spm"], sta_sum["aw"], marker="o", label="AW Active (kcal/min)")
    ax.plot(sta_sum["spm"], sta_sum["net"], marker="s", linestyle="--", label="ACSM NET (kcal/min)")

    if "efficiency_theory" in sta_sum.columns and len(sta_sum) > 0 and eff_theory_col:
        eta = float(sta_sum["efficiency_theory"].iloc[0])
        ax.text(sta_sum["spm"].min(), sta_sum["net"].min(), f"Theory eff ~ {eta:.3f}", va="bottom")

    ax.set_xlabel("Steps per minute (spm)")
    ax.set_ylabel("kcal/min")
    ax.set_title("StairMaster: Apple Watch vs ACSM NET by SPM")
    ax.legend()
    ax.grid(True, alpha=0.3)

    save_to = Path(save_to)
    save_to.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(save_to, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

    return sta_sum

# -------------------- Simple DataFrame styling --------------------

def style_table(df: pd.DataFrame, caption: str = ""):
    """Lightweight table styling that works across pandas versions."""
    if df is None or len(df) == 0:
        return pd.DataFrame().style.set_caption(caption)
    sty = df.style
    try:
        sty = sty.hide(axis="index")
    except Exception:
        try:
            sty = sty.hide_index()
        except Exception:
            pass
    return (sty
            .format(precision=2)
            .set_caption(caption)
            .set_table_styles([
                {"selector":"th","props":[("text-align","left"),("font-weight","600")]},
                {"selector":"caption","props":[("caption-side","top"),("font-weight","600"),("margin-bottom","0.5rem")]}
            ]))

__all__ = [
    "vo2_treadmill_gross_mLkgmin","vo2_stair_gross_mLkgmin",
    "kcal_per_min_from_vo2_mLkgmin","net_kcal_per_min_from_gross_vo2",
    "mech_power_treadmill_W","mech_power_stair_W","met_power_W","efficiency",
    "remove_flat_treadmill","treadmill_efficiency_plot","stair_efficiency_plot",
    "style_table"
]
