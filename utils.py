import pandas as pd
import os

CSV_FILE = "extracted_invoices.csv"

def save_to_csv(data):
    df = pd.DataFrame([data])
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)
