import pandas as pd
import os
from datetime import datetime

DATA_PATH = "data/BDD.xlsx"
REQUESTS_PATH = "data/demandes.xlsx"

DATE_COLS = ["Première MADU projet", "MES PFM1"]


def load_data():
    df = pd.read_excel(DATA_PATH, dtype=str)
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
    df["__id__"] = range(len(df))
    return df


def save_data(df: pd.DataFrame):
    df_save = df.drop(columns=["__id__"], errors="ignore")
    df_save.to_excel(DATA_PATH, index=False)


def load_requests():
    if not os.path.exists(REQUESTS_PATH):
        return pd.DataFrame(columns=[
            "id_demande", "type", "id_ligne", "details_ligne",
            "description", "date_demande", "statut"
        ])
    return pd.read_excel(REQUESTS_PATH, dtype=str)


def save_requests(df: pd.DataFrame):
    df.to_excel(REQUESTS_PATH, index=False)


def add_request(type_demande: str, id_ligne: int, details_ligne: str, description: str):
    df = load_requests()
    new_id = len(df) + 1
    new_row = {
        "id_demande": str(new_id),
        "type": type_demande,
        "id_ligne": str(id_ligne),
        "details_ligne": details_ligne,
        "description": description,
        "date_demande": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "statut": "En attente"
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_requests(df)


def apply_modification(id_ligne: int, description: str, df_data: pd.DataFrame):
    """Parse 'Colonne: valeur' lines from description and apply them."""
    for line in description.split("\n"):
        if ":" in line:
            col, val = line.split(":", 1)
            col, val = col.strip(), val.strip()
            if col in df_data.columns:
                mask = df_data["__id__"] == id_ligne
                df_data.loc[mask, col] = val
    return df_data
