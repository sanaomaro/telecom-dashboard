
import streamlit as st
from app.data_processing import load_data, clean_data
from app.visualization import summarize_data, generate_charts
from app.modeling import detect_outliers, regression_analysis, predict_snr

st.set_page_config(page_title="Cellular Network Dashboard", layout="wide")

st.title("📡 Cellular Network Performance Dashboard")
file_path = "C:/Users/SANA/Downloads/train_telecom.csv"  # Adjust this path

df = load_data(file_path)
if df is not None:
    df = clean_data(df)
    with st.sidebar:
        st.header("2. Filters")
        env_options = st.multiselect("Environment Types", options=df['Environment'].unique(), default=list(df['Environment'].unique()))
        call_options = st.multiselect("Call Types", options=df['Call Type'].unique(), default=list(df['Call Type'].unique()))
        signal_slider = st.slider("Signal Strength Range (dBm)", -120, -30, (-100, -60))

    df_filtered = df[
        df['Environment'].isin(env_options) &
        df['Call Type'].isin(call_options) &
        df['Signal Strength (dBm)'].between(signal_slider[0], signal_slider[1])
    ]

    summarize_data(df_filtered)
    generate_charts(df_filtered)
    detect_outliers(df_filtered)
    regression_analysis(df_filtered)
    predict_snr(df_filtered)
else:
    st.info("Dataset not found. Please check the file path.")
