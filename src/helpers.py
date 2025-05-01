# src/helpers.py

import pandas as pd

# File Helpers
def pdAutoRead(file_path):
    """Utility function to read CSV or Excel files."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
