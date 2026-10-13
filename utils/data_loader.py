import pandas as pd
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(
        "data/bienestar_laboral.csv",
        sep=";",
        encoding="utf-8",
    )
    # IR1 is reverse-scored: must invert before computing IR_prom.
    # Raw CSV IR_prom omits this inversion; corrected formula matches the notebook.
    if "IR1" in df.columns and all(c in df.columns for c in ["IR2", "IR3", "IR4"]):
        df["IR_prom"] = ((8 - df["IR1"]) + df["IR2"] + df["IR3"] + df["IR4"]) / 4
    return df
