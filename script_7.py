# Create a comprehensive test script to validate the entire system
test_script = '''
"""
MineGuard 3D System Test Suite
Comprehensive testing for all components
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

def test_data_generation():
    """Test synthetic data generation"""
    print("\\n🧪 Testing Data Generation...")
    
    try:
        # Check if data file exists
        if os.path.exists('synthetic_mining_data.csv'):
            data = pd.read_csv('synthetic_mining_data.csv')
            
            # Validate data structure
            expected_cols = [
                'timestamp', 'displacement_mm', 'strain_microstrain', 'vibration_hz',
                'methane_ppm', 'co_ppm', 'seismic_magnitude', 'seismic_frequency',
                'rainfall_mm', 'temperature_c', 'humidity_percent', 
                'pore_pressure_kpa', 'water_level_m',
                'rockfall_hazard', 'gas_hazard', 'seismic_hazard', 'groundwater_hazard'
            ]
            
            missing_cols = [col for col in expected_cols if col not in data.columns]
            if missing_cols:
                print(f"❌ Missing columns: {missing_cols}")
                return False
            
            print(f"✅ Data file loaded successfully ({len(data)} rows)")
            print(f"✅ All required columns present")
            print(f"✅ Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")
            
            # Check for hazard events
            hazard_cols = ['rockfall_hazard', 'gas_hazard', 'seismic_hazard', 'groundwater_hazard']
            for hazard in hazard_cols:
                count = data[hazard].sum()
                percentage = (count / len(data)) * 100
                print(f"✅ {hazard}: {count} events ({percentage:.1f}%)")
            
            return True
        else:
            print("❌ Data file not found")
            return False
    
    except Exception as e:
        print(f"❌ Error in data generation test: {e}")
        return False

def test_model_training():
    """Test ML model training and loading"""
    print("\\n🤖 Testing ML Models...")
    
    try:
        from models import MultiHazardPredictor
        
        predictor = MultiHazardPredictor()
        
        # Check if models exist
        model_dir = 'models'
        if not os.path.exists(model_dir):
            print("❌ Models directory not found")
            return False
        
        # Check for all model files
        hazard_types = ['rockfall_hazard', 'gas_hazard', 'seismic_hazard', 'groundwater_hazard']
        for hazard in hazard_types:
            model_file = f'{model_dir}/{hazard}_model.pkl'
            scaler_file = f'{model_dir}/{hazard}_scaler.pkl'
            
            if not os.path.exists(model_file):
                print(f"❌ Missing model file: {model_file}")
                return False
            if not os.path.exists(scaler_file):
                print(f"❌ Missing scaler file: {scaler_file}")
                return False
        
        print("✅ All model files found")
        
        # Test model loading
        predictor.load_models()
        print("✅ Models loaded successfully")
        
        # Test prediction with sample data
        sample_data = {
            'displacement_mm': 5.0,
            'strain_microstrain': 500.0,
            'vibration_hz': 5.0,
            'methane_ppm': 20.0,
            'co_ppm': 10.0,
            'seismic_magnitude': 0.5,
            'seismic_frequency': 5.0,
            'rainfall_mm': 2.0,
            'temperature_c': 25.0,
            'humidity_percent': 60.0,
            'pore_pressure_kpa': 150.0,
            'water_level_m': 10.0
        }
        
        predictions = predictor.predict_single(sample_data)
        
        if len(predictions) == 4:
            print("✅ Model prediction test successful")
            for hazard, pred in predictions.items():
                prob = pred['probability'][0]
                pred_class = pred['prediction'][0]
                print(f"   {hazard}: {pred_class} (prob: {prob:.3f})")
            return True
        else:
            print("❌ Incorrect number of predictions")
            return False
    
    except Exception as e:
        print(f"❌ Error in model test: {e}")
        return False

def test_data_processing():
    """Test data processing module"""
    print("\\n📊 Testing Data Processing...")
    
    try:
        from data_processing import DataProcessor
        
        processor = DataProcessor()
        
        # Test data loading
        if os.path.exists('synthetic_mining_data.csv'):
            data = processor.load_data('synthetic_mining_data.csv')
            print(f"✅ Data loaded successfully ({len(data)} rows)")
        else:
            print("❌ Data file not found")
            return False
        
        # Test recent data retrieval
        recent_data = processor.get_recent_data(24)
        print(f"✅ Recent data retrieval successful ({len(recent_data)} rows)")
        
        # Test real-time sample
        realtime_sample = processor.get_realtime_sample(5)
        print(f"✅ Real-time sample successful ({len(realtime_sample)} rows)")
        
        # Test visualization functions (without actually creating plots)
        print("✅ Data processing module functional")
        
        return True
    
    except Exception as e:
        print(f"❌ Error in data processing test: {e}")
        return False

def test_app_imports():
    """Test if all app dependencies can be imported"""
    print("\\n📦 Testing Application Dependencies...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
        
        import pandas
        print("✅ Pandas imported successfully")
        
        import numpy
        print("✅ NumPy imported successfully")
        
        import sklearn
        print("✅ scikit-learn imported successfully")
        
        import plotly
        print("✅ Plotly imported successfully")
        
        import pydeck
        print("✅ PyDeck imported successfully")
        
        import joblib
        print("✅ Joblib imported successfully")
        
        # Test custom modules
        import models
        print("✅ Models module imported successfully")
        
        import data_processing
        print("✅ Data processing module imported successfully")
        
        return True
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in import test: {e}")
        return False

def test_system_integration():
    """Test complete system integration"""
    print("\\n🔄 Testing System Integration...")
    
    try:
        from models import MultiHazardPredictor
        from data_processing import DataProcessor
        
        # Load predictor and data processor
        predictor = MultiHazardPredictor()
        processor = DataProcessor()
        
        # Load models and data
        predictor.load_models()
        data = processor.load_data('synthetic_mining_data.csv')
        
        # Get recent data
        recent_data = processor.get_recent_data(1)
        
        if not recent_data.empty:
            # Make prediction
            predictions = predictor.predict(recent_data.tail(1))
            
            # Generate alerts
            alerts = processor.create_alert_summary(predictions)
            
            # Generate recommendations
            recommendations = processor.generate_recommendations(predictions)
            
            print("✅ End-to-end system test successful")
            print(f"   Generated {len(alerts)} alerts")
            print(f"   Generated {len(recommendations)} recommendations")
            
            return True
        else:
            print("❌ No recent data available")
            return False
    
    except Exception as e:
        print(f"❌ Error in integration test: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("=" * 60)
    print("🧪 MineGuard 3D - System Test Suite")
    print("=" * 60)
    
    tests = [
        ("Data Generation", test_data_generation),
        ("ML Models", test_model_training),
        ("Data Processing", test_data_processing),
        ("Dependencies", test_app_imports),
        ("System Integration", test_system_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\\n" + "=" * 60)
    print("📋 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\\n" + "-" * 60)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\\n🎉 All tests passed! System is ready to deploy.")
    else:
        print(f"\\n⚠️ {failed} test(s) failed. Please check the issues above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
'''

# Save the test script
with open('test_system.py', 'w') as f:
    f.write(test_script)

print("✅ Created comprehensive test script: test_system.py")