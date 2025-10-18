#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile‑friendly Waist‑to‑Hip Ratio (WHR) Calculator
===================================================
One-file Streamlit web app optimized for phones:
- Big touch-friendly sliders (minimal typing)
- cm/inch toggle with automatic conversion
- Live classification using WHO thresholds
- On-page measuring guide and tips
Run:  streamlit run whr_app_mobile.py
"""

import math
import streamlit as st

# ---------------------------
# Page & style
# ---------------------------
st.set_page_config(page_title="WHR Calculator (Mobile)", page_icon="📱", layout="centered")

# Subtle CSS tweaks for larger touch targets on mobile
st.markdown(
    """
    <style>
    .stSlider > div[data-baseweb="slider"] { padding: 18px 10px 28px 10px; }
    button[kind="primary"] { padding: 0.9rem 1.2rem; font-size: 1.05rem; }
    .big-metric div[data-testid="stMetricValue"] { font-size: 2rem; }
    .stRadio > label { font-size: 1.05rem; }
    .stSelectbox > div > div { font-size: 1.05rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📱 WHR Calculator (Mobile)")
st.write(
    "Estimate your **Waist‑to‑Hip Ratio (WHR)** and WHO risk category. "
    "Use the unit toggle below — sliders adapt automatically."
)

# ---------------------------
# Helpers
# ---------------------------
def cm_to_in(x: float) -> float:
    return x / 2.54

def in_to_cm(x: float) -> float:
    return x * 2.54

def classify(sex: str, whr: float) -> str:
    s = sex.lower()
    if s == "male":
        if whr < 0.90:
            return "Low risk"
        elif whr < 1.00:
            return "Moderate risk"
        else:
            return "High risk"
    else:
        if whr < 0.80:
            return "Low risk"
        elif whr < 0.85:
            return "Moderate risk"
        else:
            return "High risk"

# ---------------------------
# Sidebar: measuring guide
# ---------------------------
with st.sidebar:
    st.header("How to measure")
    st.write(
        "• **Waist**: midway between lower rib and top of hip bone, after a normal exhale.\n"
        "• **Hips**: around the widest part of the buttocks.\n"
        "Keep the tape **horizontal**, snug, not tight."
    )
    st.info(
        "Tip: Use the **same unit** for both measurements. "
        "WHR = waist ÷ hips."
    )
    st.caption(
        "WHO thresholds — Men: <0.90 (low), 0.90–0.99 (moderate), ≥1.00 (high); "
        "Women: <0.80 (low), 0.80–0.84 (moderate), ≥0.85 (high)."
    )

# ---------------------------
# Inputs (touch‑friendly)
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    unit = st.segmented_control("Unit", options=["cm", "in"], default="cm")
with col2:
    sex = st.segmented_control("Sex", options=["Male", "Female"], default="Male")

# Sensible slider ranges for mobile use
if unit == "cm":
    waist_min, waist_max, waist_step = 50.0, 150.0, 0.5
    hip_min, hip_max, hip_step = 70.0, 170.0, 0.5
else:
    waist_min, waist_max, waist_step = cm_to_in(50.0), cm_to_in(150.0), 0.25
    hip_min, hip_max, hip_step = cm_to_in(70.0), cm_to_in(170.0), 0.25

st.subheader("Measurements")
waist = st.slider(
    f"Waist ({unit})",
    min_value=float(waist_min),
    max_value=float(waist_max),
    value=float((waist_min + waist_max) / 2),
    step=float(waist_step),
)
hip = st.slider(
    f"Hips ({unit})",
    min_value=float(hip_min),
    max_value=float(hip_max),
    value=float((hip_min + hip_max) / 2),
    step=float(hip_step),
)

# Optional quick nudge buttons for fine adjustment
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("− Waist"):
        waist = max(waist_min, waist - waist_step)
with c2:
    if st.button("+ Waist"):
        waist = min(waist_max, waist + waist_step)
with c3:
    if st.button("− Hips"):
        hip = max(hip_min, hip - hip_step)
with c4:
    if st.button("+ Hips"):
        hip = min(hip_max, hip + hip_step)

# ---------------------------
# Compute & display
# ---------------------------
if unit == "in":
    waist_cm = in_to_cm(waist)
    hip_cm = in_to_cm(hip)
else:
    waist_cm = waist
    hip_cm = hip

invalid = (waist_cm <= 0) or (hip_cm <= 0)

st.divider()
st.subheader("Results")

if invalid:
    st.error("Please provide positive measurements for both waist and hips.")
else:
    whr = waist_cm / hip_cm
    category = classify(sex, whr)

    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.metric("WHR", f"{whr:.2f}", help="Waist ÷ Hips")
    with mcol2:
        st.metric("WHO category", category)
    with mcol3:
        st.metric("Inputs", f"{sex} • {unit}")

    # Traffic‑light style messages
    if category == "Low risk":
        st.success(
            "Your WHR indicates **low cardiometabolic risk** and a favourable fat distribution pattern."
        )
    elif category == "Moderate risk":
        st.warning(
            "Your WHR indicates **moderate risk**. Consider lifestyle measures (dietary quality, resistance & aerobic activity)."
        )
    else:
        st.error(
            "Your WHR indicates **high risk** of metabolic & cardiovascular complications. "
            "Discuss with a healthcare professional alongside other tests (HbA1c, lipids, BP)."
        )

    with st.expander("Details & tips"):
        st.write(
            "- WHR captures **fat distribution**: abdominal vs hip/thigh.\n"
            "- Even with a normal BMI, a **higher WHR** increases risk.\n"
            "- Re‑measure a few times and use the **average** for accuracy."
        )

st.caption("This tool does not diagnose disease. For concerns, seek medical advice.")
