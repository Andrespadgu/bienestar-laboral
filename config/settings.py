APP_CONFIG = {
    "title": "Bienestar Laboral",
    "icon": "◼",
    "layout": "wide",
    "description": "400 trabajadores · 16 dimensiones psicosociales · Sector público y mixto",
}

DATA_CONFIG = {
    "raw_path": "data/",
    "processed_path": "data/",
}

COLORS = {
    "blue":       "#2E5A87",
    "coral":      "#C75B3C",
    "green":      "#5E8B7E",
    "amber":      "#C4820A",
    "blue_light": "#7A9BB8",
    "bg":         "#F7F2EA",
    "bg_alt":     "#EEF2F7",
    "dark":       "#0D1E2E",
    "text":       "#1C2B3A",
    "text_soft":  "#5C6E80",
}

# Dimension metadata — ire is intentionally absent; computed at runtime from real data
DIMS = [
    {"k": "SM_prom",  "lb": "Salud mental org.",      "t": "resource",   "mx": 5},
    {"k": "CT_prom",  "lb": "Control del trabajo",    "t": "resource",   "mx": 5},
    {"k": "PT_prom",  "lb": "Presión del tiempo",     "t": "demand",     "mx": 5},
    {"k": "GC_prom",  "lb": "Gestión del cambio",     "t": "resource",   "mx": 5},
    {"k": "IR_prom",  "lb": "Intención de retiro",    "t": "negative",   "mx": 7},
    {"k": "CL_prom",  "lb": "Compromiso del líder",   "t": "resource",   "mx": 5},
    {"k": "TF_prom",  "lb": "Conflicto Trabajo→Fam.", "t": "demand",     "mx": 7},
    {"k": "CoR_prom", "lb": "Conflicto de rol",       "t": "demand",     "mx": 5},
    {"k": "SOM_prom", "lb": "Somatización",           "t": "negative",   "mx": 7},
    {"k": "BU_prom",  "lb": "Burnout",                "t": "negative",   "mx": 5},
    {"k": "SAT_prom", "lb": "Satisfacción laboral",   "t": "protective", "mx": 7},
    {"k": "DL_prom",  "lb": "Desgaste laboral",       "t": "negative",   "mx": 7},
    {"k": "AC_prom",  "lb": "Apoyo de compañeros",    "t": "resource",   "mx": 5},
    {"k": "BP_prom",  "lb": "Bienestar percibido",    "t": "protective", "mx": 7},
    {"k": "FT_prom",  "lb": "Conflicto Fam.→Trabajo", "t": "demand",    "mx": 7},
    {"k": "CR_prom",  "lb": "Claridad de rol",        "t": "resource",   "mx": 5},
]

# Correlation pairs — rho / p-value are computed at runtime via utils.stats
CORR_PAIRS = [
    {"a": "SAT ↔ IR",  "cols": ("SAT_prom", "IR_prom"),  "dir": "negative"},
    {"a": "BP ↔ BU",   "cols": ("BP_prom",  "BU_prom"),  "dir": "protective"},
    {"a": "BU ↔ DL",   "cols": ("BU_prom",  "DL_prom"),  "dir": "harmful"},
    {"a": "PT ↔ BU",   "cols": ("PT_prom",  "BU_prom"),  "dir": "harmful"},
    {"a": "BU ↔ SOM",  "cols": ("BU_prom",  "SOM_prom"), "dir": "harmful"},
    {"a": "CL ↔ BU",   "cols": ("CL_prom",  "BU_prom"),  "dir": "protective"},
    {"a": "CL ↔ SAT",  "cols": ("CL_prom",  "SAT_prom"), "dir": "protective"},
    {"a": "CoR ↔ BU",  "cols": ("CoR_prom", "BU_prom"),  "dir": "harmful"},
]
