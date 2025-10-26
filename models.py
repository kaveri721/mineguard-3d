
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

class MultiHazardPredictor:
    """
    Multi-hazard AI prediction system for mining safety.
    Trains separate models for each hazard type.
    """

    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = [
            'displacement_mm', 'strain_microstrain', 'vibration_hz',
            'methane_ppm', 'co_ppm', 'seismic_magnitude', 
            'seismic_frequency', 'rainfall_mm', 'temperature_c',
            'humidity_percent', 'pore_pressure_kpa', 'water_level_m'
        ]
        self.hazard_types = ['rockfall_hazard', 'gas_hazard', 
                             'seismic_hazard', 'groundwater_hazard']

    def load_data(self, filepath):
        """Load mining sensor data from CSV"""
        self.data = pd.read_csv(filepath)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        return self.data

    def prepare_features(self, data):
        """Extract and scale features"""
        X = data[self.feature_columns].copy()

        # Handle any missing values
        X = X.fillna(X.mean())

        return X

    def train_models(self, data, test_size=0.2, random_state=42):
        """
        Train RandomForest models for each hazard type
        """
        X = self.prepare_features(data)

        results = {}

        for hazard in self.hazard_types:
            print(f"\n{'='*60}")
            print(f"Training model for: {hazard}")
            print('='*60)

            y = data[hazard]

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )

            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # Train RandomForest model
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=random_state,
                class_weight='balanced',
                n_jobs=-1
            )

            model.fit(X_train_scaled, y_train)

            # Evaluate
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)

            print(f"\nAccuracy: {accuracy:.4f}")
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))

            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)

            print("\nTop 5 Most Important Features:")
            print(feature_importance.head())

            # Store model and scaler
            self.models[hazard] = model
            self.scalers[hazard] = scaler

            results[hazard] = {
                'accuracy': accuracy,
                'feature_importance': feature_importance
            }

        return results

    def predict(self, X):
        """
        Make predictions for all hazard types
        Returns dict with predictions and probabilities
        """
        if isinstance(X, pd.DataFrame):
            X = X[self.feature_columns]

        predictions = {}

        for hazard in self.hazard_types:
            X_scaled = self.scalers[hazard].transform(X)
            pred = self.models[hazard].predict(X_scaled)
            pred_proba = self.models[hazard].predict_proba(X_scaled)[:, 1]

            predictions[hazard] = {
                'prediction': pred,
                'probability': pred_proba
            }

        return predictions

    def predict_single(self, sensor_data):
        """
        Make prediction for a single sensor reading
        sensor_data: dict with sensor values
        """
        X = pd.DataFrame([sensor_data])[self.feature_columns]
        return self.predict(X)

    def save_models(self, directory='models'):
        """Save trained models and scalers"""
        os.makedirs(directory, exist_ok=True)

        for hazard in self.hazard_types:
            model_path = os.path.join(directory, f'{hazard}_model.pkl')
            scaler_path = os.path.join(directory, f'{hazard}_scaler.pkl')

            joblib.dump(self.models[hazard], model_path)
            joblib.dump(self.scalers[hazard], scaler_path)

        print(f"\nModels saved to {directory}/")

    def load_models(self, directory='models'):
        """Load pre-trained models and scalers"""
        for hazard in self.hazard_types:
            model_path = os.path.join(directory, f'{hazard}_model.pkl')
            scaler_path = os.path.join(directory, f'{hazard}_scaler.pkl')

            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.models[hazard] = joblib.load(model_path)
                self.scalers[hazard] = joblib.load(scaler_path)
            else:
                raise FileNotFoundError(f"Model files not found for {hazard}")

        print(f"\nModels loaded from {directory}/")

def train_and_save_models(data_path='synthetic_mining_data.csv'):
    """
    Main function to train and save all models
    """
    predictor = MultiHazardPredictor()

    print("Loading data...")
    data = predictor.load_data(data_path)
    print(f"Loaded {len(data)} samples")

    print("\nTraining models...")
    results = predictor.train_models(data)

    print("\nSaving models...")
    predictor.save_models()

    return predictor, results

if __name__ == '__main__':
    predictor, results = train_and_save_models()
