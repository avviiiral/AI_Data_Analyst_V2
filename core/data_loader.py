import pandas as pd

def load_data(uploaded_file):
    """
    Load CSV, Excel or JSON automatically
    """
    
    filename = uploaded_file.name.lower()
    
    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    
    elif filename.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
    
    elif filename.endswith(".json"):
        return pd.read_json(uploaded_file)
    
    else:
        raise ValueError("Unsupported file format.")