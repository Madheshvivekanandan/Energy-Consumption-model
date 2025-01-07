import streamlit as st
import pandas as pd
import pickle  # To load the trained model

# Load the trained model
model = pickle.load(open('Energy_consumption_model.pkl', 'rb'))  # Ensure your model is saved as this

# Model Accuracy (Assumed to be known from training)
MODEL_ACCURACY = 1.0  # Update with your actual accuracy if different

# ---- 🎨 Page Configuration ----
st.set_page_config(
    page_title="Energy Consumption Predictor",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---- 🖌️ Custom CSS ----
st.markdown("""
    <style>
        .main {
            background-color: #f0f8ff;
        }
        .stTextInput, .stNumberInput, .stSelectbox {
            border-radius: 8px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .prediction-box {
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #2e7d32;
        }
        .sidebar .sidebar-content {
            background-color: #e3f2fd;
        }
    </style>
""", unsafe_allow_html=True)

# ---- 🏢 App Title ----
st.title("⚡ Energy Consumption Predictor")
st.write("Fill in the building details below to predict **Energy Consumption (kWh)**.")

# ---- 📊 Sidebar Information ----
st.sidebar.title("📊 Model Information")
st.sidebar.write(f"✅ **Model Accuracy:** `{MODEL_ACCURACY:.2f}`")
st.sidebar.write("🧠 **Model Type:** Linear Regression Model")
st.sidebar.write("📚 **Dataset:** Energy Consumption Dataset")
st.sidebar.write("📈 **Developer:** Madhesh Vivekanandan")

# ---- 📋 Input Form ----
st.write("### 📝 Enter Building Details:")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)  # Two columns for better spacing
    
    with col1:
        square_footage = st.number_input("🏠 Square Footage", min_value=0.0, step=1.0)
        number_of_occupants = st.number_input("👥 Number of Occupants", min_value=0, step=1)
        appliances_used = st.number_input("🔌 Appliances Used", min_value=0, step=1)
    
    with col2:
        average_temperature = st.number_input("🌡️ Average Temperature (°C)", min_value=-5.0, max_value=50.0, step=1.0)
        building_type = st.selectbox("🏢 Building Type", ['Residential', 'Commercial', 'Industrial'])
        day_of_week = st.selectbox("📅 Day of Week", ['Weekday', 'Weekend'])
    
    submitted = st.form_submit_button("🚀 Predict Energy Consumption")
    
# ---- ⚡ Prediction ----
if submitted:
    # Convert categorical features
    building_type_encoded = {'Residential': 0, 'Commercial': 1, 'Industrial': 2}[building_type]
    day_of_week_encoded = {'Weekday': 0, 'Weekend': 1}[day_of_week]
    
    # Create DataFrame for prediction
    input_data = pd.DataFrame({
        'Building Type': [building_type_encoded],
        'Square Footage': [square_footage],
        'Number of Occupants': [number_of_occupants],
        'Appliances Used': [appliances_used],
        'Average Temperature': [average_temperature],
        'Day of Week': [day_of_week_encoded]
    })
    
    # Make prediction
    prediction = model.predict(input_data)
    
    st.markdown(
        f"<div class='prediction-box'>⚡ Predicted Energy Consumption: {prediction[0]:.2f} kWh</div>",
        unsafe_allow_html=True
    )

