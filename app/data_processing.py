import pandas as pd

def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        return df
    except FileNotFoundError:
        return None

def clean_data(df):
    df['Tower ID'] = df['Tower ID'].astype('category')
    df['User ID'] = df['User ID'].astype('category')
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    env_map = {'open': 'rural', 'home': 'indoor', 'suburban': 'suburban', 'urban': 'urban'}
    df['Env_Std'] = df['Environment'].map(env_map)
    df['Location_Type'] = df['Env_Std'].apply(lambda x: 'indoor' if x == 'indoor' else 'outdoor')
    return df