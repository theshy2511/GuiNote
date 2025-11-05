# utils.py
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def read_input_excel(path, sheet, mssv_col='mssv'):
    df = pd.read_excel(path, sheet_name=sheet, dtype=str)
    if mssv_col not in df.columns:
        raise KeyError(f"Column '{mssv_col}' not found in {path}:{sheet}")
    return df

def write_output_excel(df, path):
    df.to_excel(path, index=False)

def get_capsolver_key():
    return os.getenv('CAPSOLVER_API_KEY')