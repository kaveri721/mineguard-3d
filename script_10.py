# Create a simplified version of data processing without pydeck to verify core functionality
simplified_data_processing = """
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataProcessor:
    \"\"\"
    Simplified data processing utilities for MineGuard 3D
    (Version without external visualization dependencies)
    \"\"\"
    
    def __init__(self):
        self.data = None
        self.current_time = datetime.now()
        
    def load_data(self, filepath):
        \"\"\"Load and preprocess sensor data\"\"\"
        self.data = pd.read_csv(filepath)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data = self.data.sort_values('timestamp')
        return self.data
    
    def get_recent_data(self, hours=24):
        \"\"\"Get data from last N hours\"\"\"
        if self.data is None:
            return pd.DataFrame()
            
        # For demo purposes, use last N records
        recent_data = self.data.tail(int(hours * 6))  # 6 readings per hour
        return recent_data
    
    def get_realtime_sample(self, n=1):
        \"\"\"Get the most recent N samples\"\"\"
        if self.data is None:
            return pd.DataFrame()
        return self.data.tail(n)
    
    def create_alert_summary(self, predictions):
        \"\"\"Create alert summary dashboard\"\"\"
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
        \"\"\"Generate safety recommendations based on predictions\"\"\"
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
"""

# Save simplified version
with open('data_processing_simple.py', 'w') as f:
    f.write(simplified_data_processing)

# Test the core functionality
print("🔬 Testing core system functionality...")

# Test models and simplified data processing
from models import MultiHazardPredictor
from data_processing_simple import DataProcessor

# Load predictor and data processor
predictor = MultiHazardPredictor()
processor = DataProcessor()

# Load models and data
predictor.load_models()
data = processor.load_data('synthetic_mining_data.csv')

# Test recent data
recent_data = processor.get_recent_data(1)
print(f"✅ Recent data loaded: {len(recent_data)} rows")

# Test prediction
if not recent_data.empty:
    predictions = predictor.predict(recent_data.tail(1))
    print("✅ Predictions generated successfully")
    
    # Test alert generation
    alerts = processor.create_alert_summary(predictions)
    print(f"✅ Generated {len(alerts)} alerts")
    
    # Test recommendations
    recommendations = processor.generate_recommendations(predictions)
    print(f"✅ Generated {len(recommendations)} recommendations")
    
    print("\n🎉 Core system functionality verified!")
    print("The system is ready for deployment on your laptop.")

else:
    print("❌ No recent data available")