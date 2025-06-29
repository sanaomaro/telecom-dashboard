# ---------------- app/visualization.py ----------------
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

def summarize_data(df):
    st.subheader("📊 Quick Network Summary")
    avg_signal = df['Signal Strength (dBm)'].mean()
    weak_areas = len(df[df['Signal Strength (dBm)'] < -95])
    worst_tower = df.groupby('Tower ID')['Signal Strength (dBm)'].mean().idxmin()
    best_env = df.groupby('Environment')['SNR'].mean().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Signal Strength", f"{avg_signal:.1f} dBm")
    col2.metric("Critical Areas", f"{weak_areas} locations")
    col3.metric("Worst Tower", worst_tower)
    col4.metric("Best Environment", best_env)

def generate_charts(df):
    st.subheader("📈 Call Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(data=df, x='Environment', hue='Call Type', palette='Set2', ax=ax)
    st.pyplot(fig)

    st.subheader("📉 Signal Strength vs. SNR")
    fig2 = px.scatter(df, x='Signal Strength (dBm)', y='SNR', color='Environment')
    st.plotly_chart(fig2)