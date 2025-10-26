
# Let's start by creating the complete MineGuard 3D project structure
# First, I'll create a synthetic dataset generator for mining hazard data

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic mining sensor data
def generate_synthetic_mining_data(n_samples=10000, save_path='synthetic_mining_data.csv'):
    """
    Generate synthetic multi-hazard mining sensor data
    """
    
    # Time series - 10000 samples over ~7 days (readings every 10 minutes)
    start_time = datetime(2025, 1, 1, 0, 0, 0)
    timestamps = [start_time + timedelta(minutes=10*i) for i in range(n_samples)]
    
    # Base sensor readings with correlations
    displacement = np.random.normal(5, 2, n_samples) + np.random.normal(0, 0.5, n_samples).cumsum() * 0.01
    displacement = np.clip(displacement, 0, 50)
    
    strain = displacement * 100 + np.random.normal(0, 50, n_samples)
    strain = np.clip(strain, 0, 5000)
    
    vibration = np.random.gamma(2, 2, n_samples) + displacement * 0.5
    vibration = np.clip(vibration, 0, 50)
    
    # Gas emissions (methane and CO)
    methane = np.random.gamma(3, 5, n_samples)
    methane = np.clip(methane, 0, 200)
    
    co = np.random.gamma(2, 3, n_samples)
    co = np.clip(co, 0, 100)
    
    # Seismic activity
    seismic_magnitude = np.random.exponential(0.5, n_samples)
    seismic_magnitude = np.clip(seismic_magnitude, 0, 5)
    
    seismic_frequency = np.random.gamma(2, 5, n_samples)
    seismic_frequency = np.clip(seismic_frequency, 0, 50)
    
    # Environmental factors
    rainfall = np.random.gamma(1.5, 2, n_samples)
    rainfall = np.clip(rainfall, 0, 50)
    
    temperature = np.random.normal(25, 5, n_samples)
    temperature = np.clip(temperature, 10, 40)
    
    humidity = np.random.normal(60, 15, n_samples)
    humidity = np.clip(humidity, 20, 100)
    
    # Groundwater
    pore_pressure = np.random.normal(150, 30, n_samples) + rainfall * 2
    pore_pressure = np.clip(pore_pressure, 50, 400)
    
    water_level = np.random.normal(10, 2, n_samples) + rainfall * 0.1
    water_level = np.clip(water_level, 5, 25)
    
    # Generate hazard labels based on sensor thresholds
    rockfall_hazard = ((displacement > 15) | (strain > 2000) | (vibration > 15)).astype(int)
    gas_hazard = ((methane > 50) | (co > 30)).astype(int)
    seismic_hazard = ((seismic_magnitude > 2.0) | (seismic_frequency > 20)).astype(int)
    groundwater_hazard = ((pore_pressure > 250) | (water_level > 15)).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'timestamp': timestamps,
        'displacement_mm': displacement,
        'strain_microstrain': strain,
        'vibration_hz': vibration,
        'methane_ppm': methane,
        'co_ppm': co,
        'seismic_magnitude': seismic_magnitude,
        'seismic_frequency': seismic_frequency,
        'rainfall_mm': rainfall,
        'temperature_c': temperature,
        'humidity_percent': humidity,
        'pore_pressure_kpa': pore_pressure,
        'water_level_m': water_level,
        'rockfall_hazard': rockfall_hazard,
        'gas_hazard': gas_hazard,
        'seismic_hazard': seismic_hazard,
        'groundwater_hazard': groundwater_hazard
    })
    
    # Save to CSV
    data.to_csv(save_path, index=False)
    print(f"Generated {n_samples} samples and saved to {save_path}")
    print(f"\nDataset summary:")
    print(f"Rockfall hazard events: {rockfall_hazard.sum()} ({100*rockfall_hazard.mean():.1f}%)")
    print(f"Gas hazard events: {gas_hazard.sum()} ({100*gas_hazard.mean():.1f}%)")
    print(f"Seismic hazard events: {seismic_hazard.sum()} ({100*seismic_hazard.mean():.1f}%)")
    print(f"Groundwater hazard events: {groundwater_hazard.sum()} ({100*groundwater_hazard.mean():.1f}%)")
    
    return data

# Generate the dataset
data = generate_synthetic_mining_data()
print("\nFirst few rows:")
print(data.head(10))
