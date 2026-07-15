import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")

# Page config
st.set_page_config(
    page_title="Breast Cancer Risk Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5faff 0%, #e1f0fb 100%); }
    .header-title { color: #005dac; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
    .header-subtitle { color: #414752; font-size: 1.1rem; margin-bottom: 2rem; }
    .prediction-result { padding: 1.5rem; border-radius: 0.75rem; margin: 1rem 0; }
    .result-benign { background: linear-gradient(135deg, #d4e3ff 0%, #a5c8ff 100%); border: 2px solid #005dac; }
    .result-malignant { background: linear-gradient(135deg, #ffd9e1 0%, #fd6c9c 100%); border: 2px solid #ab2c5d; }
    .confidence-high { color: #00a854; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# ----------------- DATA & MODEL LOADING -----------------
@st.cache_resource
def load_model():
    try:
        return joblib.load('final_model.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv')
        if "Unnamed: 32" in df.columns:
            df = df.drop("Unnamed: 32", axis=1)
        if "id" in df.columns:
            df = df.drop("id", axis=1)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_resource
def get_scaler():
    try:
        df = load_data()
        if df is not None:
            df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
            X = df.drop('diagnosis', axis=1)
            scaler = StandardScaler()
            scaler.fit(X)
            return scaler
    except Exception as e:
        st.error(f"Error creating scaler: {e}")
    return None

FEATURE_NAMES = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

BENIGN_SAMPLE = {
    'radius_mean': 12.4, 'texture_mean': 13.3, 'perimeter_mean': 82.6, 'area_mean': 474.0, 'smoothness_mean': 0.108, 'compactness_mean': 0.127, 'concavity_mean': 0.0457, 'concave points_mean': 0.0311, 'symmetry_mean': 0.197, 'fractal_dimension_mean': 0.0682,
    'radius_se': 0.271, 'texture_se': 0.897, 'perimeter_se': 1.64, 'area_se': 14.67, 'smoothness_se': 0.0041, 'compactness_se': 0.0189, 'concavity_se': 0.017, 'concave points_se': 0.00649, 'symmetry_se': 0.0168, 'fractal_dimension_se': 0.00242,
    'radius_worst': 14.5, 'texture_worst': 20.49, 'perimeter_worst': 96.09, 'area_worst': 630.5, 'smoothness_worst': 0.131, 'compactness_worst': 0.278, 'concavity_worst': 0.189, 'concave points_worst': 0.0728, 'symmetry_worst': 0.318, 'fractal_dimension_worst': 0.0818
}

MALIGNANT_SAMPLE = {
    'radius_mean': 17.99, 'texture_mean': 10.38, 'perimeter_mean': 122.8, 'area_mean': 1001.0, 'smoothness_mean': 0.1184, 'compactness_mean': 0.2776, 'concavity_mean': 0.3001, 'concave points_mean': 0.1471, 'symmetry_mean': 0.2419, 'fractal_dimension_mean': 0.07871,
    'radius_se': 1.095, 'texture_se': 0.9053, 'perimeter_se': 8.589, 'area_se': 153.4, 'smoothness_se': 0.006399, 'compactness_se': 0.04904, 'concavity_se': 0.05373, 'concave points_se': 0.01587, 'symmetry_se': 0.03003, 'fractal_dimension_se': 0.006193,
    'radius_worst': 25.38, 'texture_worst': 17.33, 'perimeter_worst': 184.6, 'area_worst': 2019.0, 'smoothness_worst': 0.1622, 'compactness_worst': 0.6656, 'concavity_worst': 0.7119, 'concave points_worst': 0.2654, 'symmetry_worst': 0.4601, 'fractal_dimension_worst': 0.1189
}

def predict(features):
    model = load_model()
    scaler = get_scaler()
    if model is None or scaler is None:
        return None, None, None
    try:
        input_df = pd.DataFrame([features])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        confidence = probabilities[prediction] * 100
        return prediction, confidence, probabilities
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None, None, None

def get_feature_importance():
    model = load_model()
    if model is None: return None
    try:
        xgb_model = model.named_estimators_['xgb']
        xgb_importance = xgb_model.feature_importances_
        importances = [{'feature': name, 'importance': imp} for name, imp in zip(FEATURE_NAMES, xgb_importance)]
        importances.sort(key=lambda x: x['importance'], reverse=True)
        return importances[:10]
    except:
        return None

# Naya Fix: Purani values memory se saaf karne ke liye
def clear_widget_states():
    for key in list(st.session_state.keys()):
        if key.startswith(('mean_', 'se_', 'worst_')):
            del st.session_state[key]

# ----------------- UI START -----------------
col1, col2 = st.columns([1, 4])
with col1: st.markdown("🏥")
with col2:
    st.markdown('<p class="header-title">Breast Cancer Risk Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Clinical Risk Assessment using AI-Powered Analysis</p>', unsafe_allow_html=True)

st.markdown("---")

st.sidebar.header("📋 Navigation")
page = st.sidebar.radio("Select Mode", ["🔮 Predictor", "📊 Data Insights", "📜 History"])

if page == "🔮 Predictor":
    
    # ----------------- BUTTONS WITH RERUN FIX -----------------
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Load Benign Sample", use_container_width=True):
            st.session_state.sample_loaded = "benign"
            clear_widget_states()
            st.rerun() # Fauran data load karega
    with col2:
        if st.button("📥 Load Malignant Sample", use_container_width=True):
            st.session_state.sample_loaded = "malignant"
            clear_widget_states()
            st.rerun() # Fauran data load karega
    with col3:
        if st.button("🆕 Clear Form", use_container_width=True):
            st.session_state.sample_loaded = None
            clear_widget_states()
            if 'prediction' in st.session_state: del st.session_state['prediction']
            st.rerun() # Fauran form saaf karega
    
    st.markdown("---")
    st.subheader("📏 Cell Nuclei Measurements")
    
    if 'sample_loaded' not in st.session_state:
        st.session_state.sample_loaded = None
    
    sample_data = None
    if st.session_state.sample_loaded == "benign":
        sample_data = BENIGN_SAMPLE
        st.info("✅ Benign sample data loaded")
    elif st.session_state.sample_loaded == "malignant":
        sample_data = MALIGNANT_SAMPLE
        st.warning("⚠️ Malignant sample data loaded")
    
    features = {}
    
    # ----------------- INPUT FIELDS -----------------
    def create_input_group(title, feature_list, prefix):
        st.subheader(title)
        c1, c2, c3 = st.columns(3)
        for i, feature in enumerate(feature_list):
            col = c1 if i % 3 == 0 else (c2 if i % 3 == 1 else c3)
            with col:
                default_val = sample_data[feature] if sample_data else 0.0
                features[feature] = st.number_input(f"{feature}", value=float(default_val), format="%.4f", key=f"{prefix}_{i}")

    create_input_group("Mean Values", FEATURE_NAMES[:10], "mean")
    create_input_group("Standard Error Values", FEATURE_NAMES[10:20], "se")
    create_input_group("Worst Values", FEATURE_NAMES[20:], "worst")
    
    st.markdown("---")
    
    # ----------------- PREDICTION -----------------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Predict Risk", use_container_width=True, type="primary"):
            with st.spinner("Analyzing cellular features..."):
                prediction, confidence, probabilities = predict(features)
                if prediction is not None:
                    st.session_state.prediction = prediction
                    st.session_state.confidence = confidence
                    st.session_state.probabilities = probabilities
    
    # ----------------- RESULTS -----------------
    if 'prediction' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Assessment Result")
        
        prediction = st.session_state.prediction
        confidence = st.session_state.confidence
        
        if prediction == 1:
            st.markdown(f"""<div class="prediction-result result-malignant"><h2>⚠️ HIGH RISK - MALIGNANT</h2><p style="font-size: 1.3rem; color: #6e0034;"><strong>Confidence Level: <span class="confidence-high">{confidence:.1f}%</span></strong></p><p style="color: #6e0034;">The model detected characteristics associated with malignancy.</p></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="prediction-result result-benign"><h2>✅ LOW RISK - BENIGN</h2><p style="font-size: 1.3rem; color: #001c3a;"><strong>Confidence Level: <span class="confidence-high">{confidence:.1f}%</span></strong></p><p style="color: #001c3a;">The model detected characteristics associated with benign cells.</p></div>""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2: st.progress(confidence / 100)
        
        st.markdown("---")
        st.subheader("🎯 Top Indicators")
        importance = get_feature_importance()
        if importance:
            for i, item in enumerate(importance[:5], 1):
                st.write(f"{i}. **{item['feature']}** ({item['importance']:.4f})")
        
        st.info("⚕️ **Medical Disclaimer:** This prediction is based on statistical modeling and is not a definitive diagnosis. Please consult with an oncologist for clinical evaluation.")

elif page == "📊 Data Insights":
    st.subheader("Dataset Overview")
    df = load_data()
    if df is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Samples", len(df))
        c2.metric("Benign Cases", (df['diagnosis'] == 'B').sum())
        c3.metric("Malignant Cases", (df['diagnosis'] == 'M').sum())
        st.markdown("---")
        st.write(df.head(10))

else:
    st.subheader("Prediction History")
    st.info("Prediction history will be displayed here. Current session has no previous predictions.")
