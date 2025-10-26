
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os

# Import our custom modules
from models import MultiHazardPredictor
from data_processing import DataProcessor

# Page configuration
st.set_page_config(
    page_title="MineGuard 3D: Unified Multi-Hazard AI Digital Twin",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hazard-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .high-risk {
        background-color: #fee2e2;
        border-left-color: #dc2626;
        color: #991b1b;
    }
    .medium-risk {
        background-color: #fef3c7;
        border-left-color: #d97706;
        color: #92400e;
    }
    .low-risk {
        background-color: #d1fae5;
        border-left-color: #059669;
        color: #065f46;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_predictor():
    """Load the trained ML models"""
    predictor = MultiHazardPredictor()
    try:
        predictor.load_models('models')
        return predictor
    except FileNotFoundError:
        st.error("Models not found! Please train models first by running: python models.py")
        return None

@st.cache_data
def load_data():
    """Load and cache the sensor data"""
    processor = DataProcessor()
    if os.path.exists('synthetic_mining_data.csv'):
        data = processor.load_data('synthetic_mining_data.csv')
        return data, processor
    else:
        st.error("Data file not found! Please ensure synthetic_mining_data.csv exists.")
        return None, None

def main():
    # Main header
    st.markdown('<h1 class="main-header">⛏️ MineGuard 3D: Unified Multi-Hazard AI Digital Twin</h1>', 
                unsafe_allow_html=True)

    # Load models and data
    predictor = load_predictor()
    data, processor = load_data()

    if predictor is None or data is None:
        st.stop()

    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")

        # Real-time toggle
        realtime_mode = st.toggle("Real-time Mode", value=True)

        # Time range selector
        time_range = st.selectbox(
            "Time Range", 
            ["Last 1 Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
            index=2
        )

        hours_map = {"Last 1 Hour": 1, "Last 6 Hours": 6, "Last 24 Hours": 24, "Last 7 Days": 168}
        selected_hours = hours_map[time_range]

        # Manual sensor input section
        st.header("🔧 Manual Sensor Input")
        st.write("Test 'What-if' scenarios:")

        # Create input widgets for each sensor
        sensor_inputs = {}

        col1, col2 = st.columns(2)

        with col1:
            sensor_inputs['displacement_mm'] = st.slider('Displacement (mm)', 0.0, 50.0, 5.0, 0.1)
            sensor_inputs['strain_microstrain'] = st.slider('Strain (μɛ)', 0, 5000, 500, 10)
            sensor_inputs['vibration_hz'] = st.slider('Vibration (Hz)', 0.0, 50.0, 5.0, 0.1)
            sensor_inputs['methane_ppm'] = st.slider('Methane (ppm)', 0.0, 200.0, 20.0, 1.0)
            sensor_inputs['co_ppm'] = st.slider('CO (ppm)', 0.0, 100.0, 10.0, 0.5)
            sensor_inputs['seismic_magnitude'] = st.slider('Seismic Magnitude', 0.0, 5.0, 0.5, 0.1)

        with col2:
            sensor_inputs['seismic_frequency'] = st.slider('Seismic Freq (Hz)', 0.0, 50.0, 5.0, 0.1)
            sensor_inputs['rainfall_mm'] = st.slider('Rainfall (mm)', 0.0, 50.0, 2.0, 0.1)
            sensor_inputs['temperature_c'] = st.slider('Temperature (°C)', 10.0, 40.0, 25.0, 0.1)
            sensor_inputs['humidity_percent'] = st.slider('Humidity (%)', 20.0, 100.0, 60.0, 1.0)
            sensor_inputs['pore_pressure_kpa'] = st.slider('Pore Pressure (kPa)', 50.0, 400.0, 150.0, 1.0)
            sensor_inputs['water_level_m'] = st.slider('Water Level (m)', 5.0, 25.0, 10.0, 0.1)

        manual_prediction_button = st.button("🔮 Run Prediction", type="primary")

    # Main content area
    if realtime_mode:
        # Auto-refresh placeholder
        refresh_placeholder = st.empty()

        # Get latest data point for real-time prediction
        latest_data = processor.get_realtime_sample(1)

        if not latest_data.empty:
            # Make prediction on latest data
            current_predictions = predictor.predict(latest_data)

            # Display current status
            st.header("🚨 Current Alert Status")

            # Create alert cards
            alerts = processor.create_alert_summary(current_predictions)

            cols = st.columns(4)
            for i, alert in enumerate(alerts):
                with cols[i]:
                    status_color = "🔴" if alert['color'] == 'red' else "🟢"
                    risk_class = "high-risk" if alert['color'] == 'red' else "low-risk"

                    st.markdown(f"""
                    <div class="hazard-card {risk_class}">
                        <h4>{status_color} {alert['hazard']}</h4>
                        <p><strong>{alert['status']}</strong></p>
                        <p>Risk: {alert['probability']:.2%}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # Manual prediction section
    if manual_prediction_button:
        st.header("🔮 Manual Prediction Results")

        # Make prediction with manual inputs
        manual_predictions = predictor.predict_single(sensor_inputs)

        # Display prediction results
        manual_alerts = processor.create_alert_summary(manual_predictions)

        cols = st.columns(4)
        for i, alert in enumerate(manual_alerts):
            with cols[i]:
                status_color = "🔴" if alert['color'] == 'red' else "🟢"
                risk_class = "high-risk" if alert['color'] == 'red' else "low-risk"

                st.markdown(f"""
                <div class="hazard-card {risk_class}">
                    <h4>{status_color} {alert['hazard']}</h4>
                    <p><strong>{alert['status']}</strong></p>
                    <p>Risk: {alert['probability']:.2%}</p>
                </div>
                """, unsafe_allow_html=True)

        # Recommendations
        recommendations = processor.generate_recommendations(manual_predictions)

        st.header("💡 Safety Recommendations")
        for rec in recommendations:
            st.write(f"• {rec}")

        # Show input values
        with st.expander("📊 Input Values Used"):
            input_df = pd.DataFrame([sensor_inputs])
            st.dataframe(input_df.T, use_container_width=True)

    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Time Series", "🌡️ Sensor Dashboard", "🗺️ 3D Mine View", "📊 Historical Analysis"])

    with tab1:
        st.header("📈 Sensor Time Series Data")

        # Sensor selection
        available_sensors = ['displacement_mm', 'strain_microstrain', 'vibration_hz', 
                           'methane_ppm', 'co_ppm', 'seismic_magnitude', 'seismic_frequency',
                           'rainfall_mm', 'temperature_c', 'humidity_percent', 
                           'pore_pressure_kpa', 'water_level_m']

        selected_sensors = st.multiselect(
            "Select sensors to display:",
            available_sensors,
            default=['displacement_mm', 'methane_ppm', 'vibration_hz', 'seismic_magnitude']
        )

        if selected_sensors:
            try:
                fig = processor.create_time_series_plot(selected_sensors, selected_hours)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating time series plot: {e}")

    with tab2:
        st.header("🌡️ Current Sensor Readings")

        # Get recent data
        recent_data = processor.get_recent_data(selected_hours)

        if not recent_data.empty:
            # Latest readings
            latest = recent_data.iloc[-1]

            # Create metrics display
            sensor_cols = st.columns(4)
            sensors = [
                ('displacement_mm', 'Displacement', 'mm'),
                ('methane_ppm', 'Methane', 'ppm'), 
                ('vibration_hz', 'Vibration', 'Hz'),
                ('temperature_c', 'Temperature', '°C')
            ]

            for i, (sensor, label, unit) in enumerate(sensors):
                with sensor_cols[i]:
                    value = latest[sensor]
                    st.metric(
                        label=f"{label} ({unit})",
                        value=f"{value:.2f}",
                        delta=f"{value - recent_data[sensor].mean():.2f}" if len(recent_data) > 1 else None
                    )

            # Additional metrics
            more_sensors = [
                ('strain_microstrain', 'Strain', 'μɛ'),
                ('seismic_magnitude', 'Seismic Mag', ''),
                ('pore_pressure_kpa', 'Pore Pressure', 'kPa'),
                ('humidity_percent', 'Humidity', '%')
            ]

            sensor_cols2 = st.columns(4)
            for i, (sensor, label, unit) in enumerate(more_sensors):
                with sensor_cols2[i]:
                    value = latest[sensor]
                    st.metric(
                        label=f"{label} ({unit})",
                        value=f"{value:.2f}",
                        delta=f"{value - recent_data[sensor].mean():.2f}" if len(recent_data) > 1 else None
                    )

    with tab3:
        st.header("🗺️ 3D Mine Digital Twin")

        try:
            # Create 3D visualization
            predictions_df = pd.DataFrame()  # Placeholder for now
            fig_3d = processor.create_3d_mine_visualization(predictions_df)
            st.plotly_chart(fig_3d, use_container_width=True)

            st.info("💡 This 3D visualization shows synthetic mine tunnel points colored by risk level. "
                   "In a real implementation, this would show actual mine geometry and real-time sensor locations.")

        except Exception as e:
            st.error(f"Error creating 3D visualization: {e}")

    with tab4:
        st.header("📊 Historical Hazard Analysis")

        if not data.empty:
            # Historical hazard statistics
            hazard_cols = ['rockfall_hazard', 'gas_hazard', 'seismic_hazard', 'groundwater_hazard']
            hazard_counts = data[hazard_cols].sum()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Hazard Event Counts")
                for hazard, count in hazard_counts.items():
                    percentage = (count / len(data)) * 100
                    st.write(f"**{hazard.replace('_hazard', '').title()}**: {count} events ({percentage:.2f}%)")

            with col2:
                st.subheader("Recent Activity")
                recent = processor.get_recent_data(24)
                if not recent.empty:
                    recent_hazards = recent[hazard_cols].sum()
                    st.write("**Last 24 hours:**")
                    for hazard, count in recent_hazards.items():
                        st.write(f"• {hazard.replace('_hazard', '').title()}: {count} events")

            # Data summary
            st.subheader("Dataset Overview")
            st.write(f"Total records: {len(data):,}")
            st.write(f"Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")
            st.write(f"Sampling interval: ~10 minutes")

    # Footer
    st.markdown("---")
    st.markdown("**MineGuard 3D** - Advanced AI-Powered Mining Safety System | Built with Streamlit & scikit-learn")

    # Auto-refresh for real-time mode
    if realtime_mode:
        time.sleep(2)
        st.rerun()

if __name__ == "__main__":
    main()
