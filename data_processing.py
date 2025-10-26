
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pydeck as pdk
from datetime import datetime, timedelta

class DataProcessor:
    """
    Data processing and visualization utilities for MineGuard 3D
    """

    def __init__(self):
        self.data = None
        self.current_time = datetime.now()

    def load_data(self, filepath):
        """Load and preprocess sensor data"""
        self.data = pd.read_csv(filepath)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data = self.data.sort_values('timestamp')
        return self.data

    def get_recent_data(self, hours=24):
        """Get data from last N hours"""
        if self.data is None:
            return pd.DataFrame()

        cutoff_time = self.current_time - timedelta(hours=hours)
        # For demo purposes, use last N records
        recent_data = self.data.tail(int(hours * 6))  # 6 readings per hour
        return recent_data

    def get_realtime_sample(self, n=1):
        """Get the most recent N samples"""
        if self.data is None:
            return pd.DataFrame()
        return self.data.tail(n)

    def create_time_series_plot(self, sensor_cols=None, hours=24):
        """Create time series plots for selected sensors"""
        recent_data = self.get_recent_data(hours)

        if recent_data.empty:
            return go.Figure().add_annotation(text="No data available")

        if sensor_cols is None:
            sensor_cols = ['displacement_mm', 'methane_ppm', 'vibration_hz', 'seismic_magnitude']

        # Create subplots
        fig = make_subplots(
            rows=len(sensor_cols), cols=1,
            subplot_titles=[col.replace('_', ' ').title() for col in sensor_cols],
            shared_xaxes=True
        )

        for i, col in enumerate(sensor_cols):
            fig.add_trace(
                go.Scatter(
                    x=recent_data['timestamp'],
                    y=recent_data[col],
                    mode='lines',
                    name=col,
                    line=dict(width=2)
                ),
                row=i+1, col=1
            )

        fig.update_layout(
            height=150 * len(sensor_cols),
            title_text="Sensor Time Series Data",
            showlegend=False
        )
        fig.update_xaxes(title_text="Time", row=len(sensor_cols), col=1)

        return fig

    def create_hazard_heatmap(self, predictions_df):
        """Create hazard risk heatmap"""
        hazard_types = ['rockfall_hazard', 'gas_hazard', 'seismic_hazard', 'groundwater_hazard']

        # Prepare data for heatmap
        heatmap_data = []
        for hazard in hazard_types:
            if f'{hazard}_prob' in predictions_df.columns:
                heatmap_data.append(predictions_df[f'{hazard}_prob'].values)

        if not heatmap_data:
            return go.Figure().add_annotation(text="No prediction data available")

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            y=[h.replace('_hazard', '').title() for h in hazard_types],
            x=predictions_df.index if not predictions_df.empty else [],
            colorscale='RdYlGn_r',
            zmin=0, zmax=1
        ))

        fig.update_layout(
            title="Hazard Risk Levels",
            xaxis_title="Time Index",
            yaxis_title="Hazard Type",
            height=300
        )

        return fig

    def create_3d_mine_visualization(self, predictions_df=None):
        """Create 3D mine visualization with hazard zones"""
        # Generate synthetic 3D mine coordinates
        np.random.seed(42)
        n_points = 100

        # Mine tunnel/chamber coordinates
        x = np.random.uniform(-100, 100, n_points)
        y = np.random.uniform(-50, 50, n_points) 
        z = np.random.uniform(-200, -10, n_points)  # Underground

        # Simulate hazard risk levels
        if predictions_df is not None and not predictions_df.empty:
            # Use actual predictions for risk coloring
            risk_levels = predictions_df.iloc[-n_points:]['rockfall_hazard_prob'].values if len(predictions_df) >= n_points else np.random.random(n_points)
        else:
            risk_levels = np.random.random(n_points)

        fig = go.Figure(data=go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=8,
                color=risk_levels,
                colorscale='RdYlGn_r',
                colorbar=dict(title="Risk Level"),
                opacity=0.8,
                line=dict(color='black', width=2)
            ),
            text=[f'Point {i}<br>Risk: {risk:.3f}' for i, risk in enumerate(risk_levels)],
            name='Mine Points'
        ))

        fig.update_layout(
            title="3D Mine Digital Twin - Risk Visualization",
            scene=dict(
                xaxis_title='X (meters)',
                yaxis_title='Y (meters)', 
                zaxis_title='Z (meters - depth)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            height=600
        )

        return fig

    def create_alert_summary(self, predictions):
        """Create alert summary dashboard"""
        alerts = []

        hazard_names = {
            'rockfall_hazard': 'Rockfall',
            'gas_hazard': 'Gas Emission', 
            'seismic_hazard': 'Seismic Activity',
            'groundwater_hazard': 'Groundwater Ingress'
        }

        for hazard_type, pred_data in predictions.items():
            probability = pred_data['probability'][0] if len(pred_data['probability']) > 0 else 0
            prediction = pred_data['prediction'][0] if len(pred_data['prediction']) > 0 else 0

            status = "HIGH RISK" if prediction == 1 else "NORMAL"
            color = "red" if prediction == 1 else "green"

            alerts.append({
                'hazard': hazard_names.get(hazard_type, hazard_type),
                'status': status,
                'probability': probability,
                'color': color
            })

        return alerts

    def generate_recommendations(self, predictions):
        """Generate safety recommendations based on predictions"""
        recommendations = []

        for hazard_type, pred_data in predictions.items():
            prediction = pred_data['prediction'][0] if len(pred_data['prediction']) > 0 else 0
            probability = pred_data['probability'][0] if len(pred_data['probability']) > 0 else 0

            if prediction == 1:
                if hazard_type == 'rockfall_hazard':
                    recommendations.extend([
                        "🚨 EVACUATE affected areas immediately",
                        "📋 Inspect rock bolts and support systems", 
                        "🔍 Increase monitoring frequency",
                        "⛔ Restrict access to high-risk zones"
                    ])
                elif hazard_type == 'gas_hazard':
                    recommendations.extend([
                        "💨 Activate ventilation systems immediately",
                        "🚨 Evacuate personnel from affected areas",
                        "🔍 Check gas detection equipment",
                        "📞 Contact emergency response team"
                    ])
                elif hazard_type == 'seismic_hazard':
                    recommendations.extend([
                        "🌍 Monitor for aftershocks",
                        "🔍 Inspect structural integrity",
                        "📋 Check seismic monitoring equipment",
                        "⚠️ Prepare for potential evacuations"
                    ])
                elif hazard_type == 'groundwater_hazard':
                    recommendations.extend([
                        "💧 Activate water pumping systems", 
                        "🔍 Monitor water levels closely",
                        "📋 Inspect drainage systems",
                        "⚠️ Prepare waterproofing measures"
                    ])
            elif probability > 0.5:
                recommendations.append(f"⚠️ Monitor {hazard_type.replace('_hazard', '')} conditions closely")

        if not recommendations:
            recommendations = ["✅ All systems normal - continue routine operations"]

        return list(set(recommendations))  # Remove duplicates
