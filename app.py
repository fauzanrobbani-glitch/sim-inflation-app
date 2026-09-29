import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from agents import (
    PaymentAdoptionAgent,
    CoreInflationAgent,
    StressTesterAgent,
    SimCityAdvisorAgent
)

# ---------------------------------------------------------
# Page Config & Custom SimCity CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="SIM-INFLATION: SimCity Regional Simulator",
    page_icon="🏙️",
    layout="wide"
)

# CSS Custom untuk Antarmuka SimCity Built
st.markdown("""
<style>
    /* Dark Neon Theme */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* SimCity Top HUD Bar */
    .hud-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        border: 2px solid #38bdf8;
        border-radius: 12px;
        padding: 15px 25px;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }
    
    .hud-title {
        color: #38bdf8;
        font-weight: 800;
        font-size: 24px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0;
    }
    
    /* Stat Cards / Metric Boxes */
    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #00f2fe;
    }
    
    .stat-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #8b949e;
        letter-spacing: 1px;
    }
    
    /* SimCity Advisor Dialogue Box */
    .advisor-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 6px solid #f59e0b;
        border-radius: 8px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    .advisor-avatar {
        font-size: 40px;
        float: left;
        margin-right: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Initialize Agents
# ---------------------------------------------------------
payment_agent = PaymentAdoptionAgent()
inflation_agent = CoreInflationAgent()
stress_agent = StressTesterAgent()
advisor_agent = SimCityAdvisorAgent()

# ---------------------------------------------------------
# Sidebar - City & Scenario Controls
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/isometric-shipping/100/city-buildings.png", width=80)
st.sidebar.title("🎮 City Control Panel")
st.sidebar.markdown("---")

city_name = st.sidebar.selectbox("Pilih Wilayah/Kota:", ["Pematangsiantar", "Medan", "Surakarta", "Balikpapan"])

st.sidebar.subheader("⚙️ Baseline Ekonomi")
base_inflation = st.sidebar.slider("Baseline Inflasi Inti (% YoY)", 1.0, 4.0, 2.1, 0.1)
base_qris = st.sidebar.slider("Adopsi QRIS/Digital Awal (%)", 10, 90, 55)
base_cash = st.sidebar.slider("Penggunaan Uang Kartal Awal (%)", 10, 90, 45)

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Kebijakan & Stress Test (Intervensi)")

scenario_preset = st.sidebar.radio(
    "Pilih Skenario Kebijakan:",
    ["Normal / Tanpa Intervensi", "Program Digitalisasi UMKM (Serbu QRIS)", "Musim Liburan/Lebaran (Demand Shock)", "Infrastruktur Kas Keliling (Non-Digital)"]
)

# Preset Adjustments
if scenario_preset == "Program Digitalisasi UMKM (Serbu QRIS)":
    qris_delta = st.sidebar.slider("Tambahan Adopsi QRIS (+%)", 0, 40, 25)
    cash_delta = st.sidebar.slider("Perubahan Uang Kartal (%)", -30, 10, -15)
    seasonal_shock = st.sidebar.slider("Guncangan Musiman", 0.0, 2.0, 0.2)
    policy_name = "Digitalisasi Pasar & UMKM"
elif scenario_preset == "Musim Liburan/Lebaran (Demand Shock)":
    qris_delta = st.sidebar.slider("Tambahan Adopsi QRIS (+%)", 0, 40, 15)
    cash_delta = st.sidebar.slider("Perubahan Uang Kartal (%)", -30, 30, 20)
    seasonal_shock = st.sidebar.slider("Guncangan Musiman", 0.0, 2.0, 1.5)
    policy_name = "Lonjakan Transaksi High-Season"
elif scenario_preset == "Infrastruktur Kas Keliling (Non-Digital)":
    qris_delta = st.sidebar.slider("Tambahan Adopsi QRIS (+%)", 0, 40, 5)
    cash_delta = st.sidebar.slider("Perubahan Uang Kartal (%)", -30, 30, 25)
    seasonal_shock = st.sidebar.slider("Guncangan Musiman", 0.0, 2.0, 0.4)
    policy_name = "Perluasan Akses Uang Fisik (PUR)"
else:
    qris_delta = 0
    cash_delta = 0
    seasonal_shock = 0.0
    policy_name = "Baseline Operations"

# ---------------------------------------------------------
# Run Multi-Agent Execution Loop
# ---------------------------------------------------------
new_qris, new_cash, velocity_index = payment_agent.process_policy(qris_delta, cash_delta, base_qris, base_cash)
sim_inflation, demand_effect, shock_effect = inflation_agent.calculate_inflation(base_inflation, velocity_index, seasonal_shock)
status, status_color, status_msg, resilience = stress_agent.evaluate_risk(sim_inflation, new_qris)
brief_text = advisor_agent.generate_brief(city_name, status, sim_inflation, new_qris, policy_name)

# ---------------------------------------------------------
# Main UI Layout (SimCity HUD)
# ---------------------------------------------------------

# Top HUD Header
st.markdown(f"""
<div class="hud-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div class="hud-title">🏙️ SIM-CITY REGIONAL SIMULATOR: {city_name.upper()}</div>
            <small style="color: #9ca3af;">System Status: Agentic AI Active | Framework: LangGraph Hybrid Engine</small>
        </div>
        <div style="background: {status_color}; color: #000; font-weight: bold; padding: 6px 16px; border-radius: 20px;">
            STATUS: {status}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">📈 Proyeksi Inflasi Inti</div>
        <div class="stat-value" style="color: {status_color};">{sim_inflation}% <small style="font-size:14px;">YoY</small></div>
        <small style="color: #6b7280;">Baseline: {base_inflation}%</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">📱 Indeks QRIS / Digital</div>
        <div class="stat-value">{new_qris:.1f}%</div>
        <small style="color: #10b981;">Δ +{qris_delta}%</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">💵 Transaksi Uang Kartal</div>
        <div class="stat-value">{new_cash:.1f}%</div>
        <small style="color: #f59e0b;">Δ {cash_delta}%</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">⚡ Perputaran Uang (Velocity)</div>
        <div class="stat-value">{velocity_index:.2f}x</div>
        <small style="color: #6366f1;">Ketahanan: {resilience}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Visualizations & Charts
# ---------------------------------------------------------
left_chart, right_chart = st.columns([6, 4])

with left_chart:
    st.subheader("📊 Simulasi Trajektori Inflasi Inti (12 Bulan ke Depan)")
    
    # Generate 12 Months Projection Trend
    months = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"]
    base_trend = [base_inflation + np.sin(i/2)*0.2 for i in range(12)]
    sim_trend = [sim_inflation + np.sin(i/2)*0.25 + (0.1 if i in [3,11] else 0) for i in range(12)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=base_trend, mode='lines+markers', name='Baseline (Tanpa Kebijakan)', line=dict(color='#6b7280', dash='dash')))
    fig.add_trace(go.Scatter(x=months, y=sim_trend, mode='lines+markers', name='Proyeksi Skenario Kebijakan', line=dict(color='#00f2fe', width=3)))
    
    # Threshold lines
    fig.add_hline(y=3.5, line_dash="dot", line_color="#EF4444", annotation_text="Batas Atas Target Inflasi (3.5%)")
    fig.add_hline(y=1.5, line_dash="dot", line_color="#10B981", annotation_text="Batas Bawah Target Inflasi (1.5%)")

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

with right_chart:
    st.subheader("🧱 Breakdown Faktor Transmisi")
    
    categories = ['Baseline', 'Efek Perputaran Uang Digital', 'Guncangan Musiman']
    values = [base_inflation, demand_effect, shock_effect]
    
    fig_bar = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation='h',
        marker=dict(color=['#3b82f6', '#8b5cf6', '#ec4899'])
    ))
    
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Kontribusi terhadap Inflasi (% YoY)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# SimCity Advisor Pop-Up Box
# ---------------------------------------------------------
st.markdown(f"""
<div class="advisor-box">
    <div class="advisor-avatar">👨‍💼</div>
    <div>
        <h4 style="margin:0; color: #f59e0b;">Laporan Penasihat Kota (SimCity Advisor Agent)</h4>
        <p style="margin-top: 8px; font-size: 15px; line-height: 1.5;">{brief_text}</p>
        <small style="color: #9ca3af;">💡 <b>Rekomendasi Agent:</b> {status_msg}</small>
    </div>
</div>
""", unsafe_allow_html=True)