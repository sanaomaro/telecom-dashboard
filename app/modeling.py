# ---------------- app/modeling.py ----------------
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import streamlit as st

def detect_outliers(df):
    st.subheader("🚨 Outlier Detection")
    df['SNR_Outlier'] = (df['SNR'] < 10) | (df['SNR'] > 40)
    df['Distance_Outlier'] = (df['Distance to Tower (km)'] > 30) | (df['Distance to Tower (km)'] < 0.1)
    df['ML_Outlier'] = IsolationForest(contamination=0.05, random_state=42).fit_predict(df[['SNR', 'Distance to Tower (km)']].abs()) == -1
    df['Total_Outlier'] = df['SNR_Outlier'] | df['Distance_Outlier'] | df['ML_Outlier']
    st.write(f"Total Outliers Detected: {df['Total_Outlier'].sum()}")
    return df

def regression_analysis(df):
    st.subheader("📊 Regression: Signal vs Distance + Attenuation")
    df = df.dropna(subset=['Distance to Tower (km)', 'Attenuation', 'Signal Strength (dBm)'])
    X = df[['Distance to Tower (km)', 'Attenuation']]
    y = df['Signal Strength (dBm)']
    model = LinearRegression().fit(X, y)
    st.write(f"Signal loss per km: {model.coef_[0]:.2f} dBm/km")
    st.write(f"Signal loss per dB attenuation: {model.coef_[1]:.2f} dBm")
    fig = px.scatter(df, x='Distance to Tower (km)', y='Signal Strength (dBm)', color='Environment')
    st.plotly_chart(fig)

def predict_snr(df):
    st.subheader("🔮 SNR Prediction using Random Forest")
    features = ['Distance to Tower (km)', 'Attenuation', 'Signal Strength (dBm)', 'Transmitted Data (MB)', 'Noise (dB)']
    df = df.dropna(subset=features + ['SNR'])
    X = df[features]
    y = df['SNR']
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    st.write(f"R² Score: {r2_score(y_test, y_pred):.3f}")
    st.write(f"MSE: {mean_squared_error(y_test, y_pred):.2f}")
    fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'True SNR', 'y': 'Predicted SNR'}, title="Predicted vs True SNR")
    fig.add_shape(type='line', x0=y_test.min(), y0=y_test.min(), x1=y_test.max(), y1=y_test.max(), line=dict(color='Red', dash='dash'))
    st.plotly_chart(fig)