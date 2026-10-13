"""
Centralized statistical computation layer.
All metrics, correlations, IRE values and KPIs are calculated here
from the real dataframe — nothing hardcoded.
"""
import numpy as np
import pandas as pd
from scipy import stats as sp
import streamlit as st
from config.settings import DIMS, CORR_PAIRS


# ── IRE ──────────────────────────────────────────────────────────────────────

@st.cache_data
def compute_ire(df: pd.DataFrame) -> list:
    """
    Compute IRE (Índice de Riesgo Estandarizado, 0–100) for all 16 dimensions.
    Resources/protective: IRE = (max - mean) / (max - 1) * 100  [low = bad]
    Demands/negative:     IRE = (mean - 1) / (max - 1) * 100    [high = bad]
    Returns list sorted by IRE descending.
    """
    result = []
    for d in DIMS:
        col = d["k"]
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if len(series) == 0:
            continue
        mean = series.mean()
        mx = d["mx"]
        if d["t"] in ("resource", "protective"):
            ire = (mx - mean) / (mx - 1) * 100
        else:
            ire = (mean - 1) / (mx - 1) * 100
        result.append({**d, "mean": round(mean, 3), "ire": round(ire, 2), "n": len(series)})
    result.sort(key=lambda x: x["ire"], reverse=True)
    return result


# ── CORRELATIONS ─────────────────────────────────────────────────────────────

@st.cache_data
def compute_correlations(df: pd.DataFrame) -> list:
    """
    Compute Spearman correlations for all CORR_PAIRS using real data.
    Returns list sorted by |rho| descending.
    """
    result = []
    for pair in CORR_PAIRS:
        col_a, col_b = pair["cols"]
        if col_a not in df.columns or col_b not in df.columns:
            continue
        data = df[[col_a, col_b]].dropna()
        if len(data) < 10:
            continue
        rho, pval = sp.spearmanr(data[col_a], data[col_b])
        result.append({
            **pair,
            "rho":  round(float(rho), 4),
            "pval": float(pval),
            "n":    len(data),
        })
    result.sort(key=lambda x: abs(x["rho"]), reverse=True)
    return result


def spearman(df: pd.DataFrame, col_a: str, col_b: str) -> tuple:
    """Return (rho, pval) for a single Spearman correlation. Not cached — call inline."""
    data = df[[col_a, col_b]].dropna()
    if len(data) < 5:
        return (float("nan"), float("nan"))
    rho, pval = sp.spearmanr(data[col_a], data[col_b])
    return round(float(rho), 4), float(pval)


# ── KPIs ─────────────────────────────────────────────────────────────────────

@st.cache_data
def compute_kpis(df: pd.DataFrame) -> dict:
    """All dashboard KPIs computed from the actual dataframe."""
    n = len(df)
    if n == 0:
        return {}

    bu  = df["BU_prom"].dropna()
    ir  = df["IR_prom"].dropna()
    som = df["SOM_prom"].dropna()
    sat = df["SAT_prom"].dropna()
    dl  = df["DL_prom"].dropna()
    bp  = df["BP_prom"].dropna()
    cl  = df["CL_prom"].dropna()
    pt  = df["PT_prom"].dropna()

    pct_bu      = (bu > 3).mean() * 100
    pct_bu_high = (bu > 3.5).mean() * 100
    pct_ir      = (ir > 4.5).mean() * 100
    pct_som     = (som > 4).mean() * 100
    pct_sat_low = (sat < 3.5).mean() * 100
    pct_dl_high = (dl > 4.5).mean() * 100

    # Leadership split
    mask_cl_high = df["CL_prom"] > 3.5
    cl_high_bu = df.loc[mask_cl_high, "BU_prom"].mean() if mask_cl_high.any() else float("nan")
    cl_low_bu  = df.loc[~mask_cl_high, "BU_prom"].mean() if (~mask_cl_high).any() else float("nan")
    cl_diff_pct = (
        (cl_low_bu - cl_high_bu) / cl_high_bu * 100
        if (not np.isnan(cl_high_bu) and cl_high_bu > 0) else float("nan")
    )

    # Correlations (computed inline for KPI display)
    rho_sat_ir,  _ = spearman(df, "SAT_prom", "IR_prom")
    rho_bu_som,  _ = spearman(df, "BU_prom",  "SOM_prom")
    rho_cl_bu,   _ = spearman(df, "CL_prom",  "BU_prom")
    rho_cl_sat,  _ = spearman(df, "CL_prom",  "SAT_prom")
    rho_pt_bu,   _ = spearman(df, "PT_prom",  "BU_prom")
    rho_bp_bu,   _ = spearman(df, "BP_prom",  "BU_prom")
    rho_bu_dl,   _ = spearman(df, "BU_prom",  "DL_prom")

    # Top 3 dims by IRE
    dims_sorted = compute_ire(df)
    top3 = dims_sorted[:3] if len(dims_sorted) >= 3 else dims_sorted
    top1 = dims_sorted[0] if dims_sorted else {}
    bottom1 = dims_sorted[-1] if dims_sorted else {}

    # Horas
    h = df["Horas_Semana"].dropna()
    pct_over48 = (h > 48).mean() * 100
    mean_hours = h.mean()

    return {
        "n":              n,
        "pct_bu":         round(pct_bu, 1),
        "pct_bu_high":    round(pct_bu_high, 1),
        "pct_ir":         round(pct_ir, 1),
        "pct_som":        round(pct_som, 1),
        "pct_sat_low":    round(pct_sat_low, 1),
        "pct_dl_high":    round(pct_dl_high, 1),
        "mean_bu":        round(bu.mean(), 2),
        "mean_sat":       round(sat.mean(), 2),
        "mean_ir":        round(ir.mean(), 2),
        "mean_dl":        round(dl.mean(), 2),
        "mean_bp":        round(bp.mean(), 2),
        "mean_cl":        round(cl.mean(), 2),
        "mean_pt":        round(pt.mean(), 2),
        "cl_high_bu":     round(cl_high_bu, 2),
        "cl_low_bu":      round(cl_low_bu, 2),
        "cl_diff_pct":    round(cl_diff_pct, 1),
        "n_cl_high":      int(mask_cl_high.sum()),
        "n_cl_low":       int((~mask_cl_high).sum()),
        "rho_sat_ir":     rho_sat_ir,
        "rho_bu_som":     rho_bu_som,
        "rho_cl_bu":      rho_cl_bu,
        "rho_cl_sat":     rho_cl_sat,
        "rho_pt_bu":      rho_pt_bu,
        "rho_bp_bu":      rho_bp_bu,
        "rho_bu_dl":      rho_bu_dl,
        "pct_over48":     round(pct_over48, 1),
        "mean_hours":     round(mean_hours, 1),
        "top3_dims":      top3,
        "top1_dim":       top1,
        "bottom1_dim":    bottom1,
        "dims_sorted":    dims_sorted,
    }


# ── GROUP COMPARISONS ─────────────────────────────────────────────────────────

@st.cache_data
def compare_groups(df: pd.DataFrame, group_col: str, metric_col: str,
                   threshold: float | None = None) -> dict:
    """
    Compare metric across all groups in group_col.
    Returns {group: {mean, n, pct_above_threshold (if threshold given)}}
    """
    groups = df[group_col].dropna().unique()
    result = {}
    for g in groups:
        sub = df[df[group_col] == g][metric_col].dropna()
        entry = {"mean": round(sub.mean(), 3), "n": len(sub)}
        if threshold is not None:
            entry["pct_above"] = round((sub > threshold).mean() * 100, 1)
        result[str(g)] = entry
    return result


def pval_label(p: float) -> str:
    """Human-readable significance label."""
    if p < 0.001:
        return "p < 0.001"
    if p < 0.01:
        return f"p = {p:.3f}"
    return f"p = {p:.3f}"
