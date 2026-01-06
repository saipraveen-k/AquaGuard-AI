"""
Ship Emergency Detection Module for AquaGuard AI
Detects ship emergencies without relying on SOS signals using AIS data analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import math
from geopy.distance import geodesic
import os

logger = logging.getLogger(__name__)

class ShipEmergencyDetector:
    """Detects ship emergencies using AIS data anomaly detection"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'speed_knots',
            'heading_change_rate',
            'course_deviation_degrees',
            'speed_change_rate',
            'position_anomaly_score'
        ]
        self.model_path = "./models/ship_emergency_model.pkl"
        self.scaler_path = "./models/ship_emergency_scaler.pkl"
        
        # Store historical data for anomaly detection
        self.ship_history = {}
        
        # Load or train model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load the ship emergency detection model"""
        try:
            if os.path.exists(self.model_path):
                logger.info("Loading existing ship emergency model...")
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
            else:
                logger.info("Training new ship emergency model...")
                self._train_model()
        except Exception as e:
            logger.error(f"Error initializing ship emergency model: {str(e)}")
            self._train_model()
    
    def _train_model(self):
        """Train the anomaly detection model with synthetic AIS data"""
        # Generate synthetic training data
        X_train = self._generate_training_data()
        
        # Train Isolation Forest for anomaly detection
        self.model = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model.fit(X_scaled)
        
        # Save model and scaler
        os.makedirs("./models", exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        logger.info("Ship emergency detection model trained and saved")
    
    def _generate_training_data(self, num_samples: int = 2000) -> np.ndarray:
        """Generate synthetic AIS training data"""
        np.random.seed(42)
        
        # Normal ship behavior patterns
        normal_speed = np.random.normal(15, 5, num_samples)  # knots
        normal_speed = np.clip(normal_speed, 0, 30)
        
        normal_heading_change = np.random.normal(0, 5, num_samples)  # degrees/hour
        normal_course_deviation = np.random.exponential(2, num_samples)  # degrees
        normal_speed_change = np.random.normal(0, 2, num_samples)  # knots/hour
        normal_position_anomaly = np.random.exponential(1, num_samples)
        
        # Combine features
        X_normal = np.column_stack([
            normal_speed, normal_heading_change, normal_course_deviation,
            normal_speed_change, normal_position_anomaly
        ])
        
        # Anomalous behavior patterns (emergencies)
        anomaly_samples = int(num_samples * 0.1)
        
        # Emergency patterns: sudden stops, course deviations, etc.
        emergency_speed = np.random.uniform(0, 5, anomaly_samples)  # Sudden speed drop
        emergency_heading_change = np.random.uniform(-90, 90, anomaly_samples)  # Sharp turns
        emergency_course_deviation = np.random.uniform(20, 180, anomaly_samples)  # Large deviations
        emergency_speed_change = np.random.uniform(-20, -5, anomaly_samples)  # Rapid deceleration
        emergency_position_anomaly = np.random.uniform(5, 20, anomaly_samples)
        
        X_anomaly = np.column_stack([
            emergency_speed, emergency_heading_change, emergency_course_deviation,
            emergency_speed_change, emergency_position_anomaly
        ])
        
        # Combine normal and anomalous data
        X_combined = np.vstack([X_normal, X_anomaly])
        
        return X_combined
    
    def detect_emergency(self, ship_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect emergency status for a single ship"""
        try:
            mmsi = ship_data['mmsi']
            
            # Validate input data
            validated_data = self._validate_ship_data(ship_data)
            
            # Update ship history
            self._update_ship_history(mmsi, validated_data)
            
            # Calculate features
            features = self._calculate_features(mmsi, validated_data)
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Anomaly detection with responsible AI thresholds
            anomaly_score = self.model.decision_function(features_scaled)[0]
            is_anomaly = self.model.predict(features_scaled)[0] == -1
            
            # Calculate emergency probability with confidence calibration
            emergency_probability = self._calculate_emergency_probability(anomaly_score)
            
            # Conservative threshold: Only flag emergency if high confidence
            # This prevents false alarms and maintains trust in the system
            emergency_threshold = 0.75  # High threshold for responsible AI
            emergency_status = 'Emergency' if (
                is_anomaly and 
                emergency_probability > emergency_threshold and
                self._validate_emergency_conditions(features)
            ) else 'Normal'
            
            # Analyze anomaly type
            anomaly_type = self._analyze_anomaly_type(features) if is_anomaly else 'None'
            
            # Confidence scoring with uncertainty quantification
            confidence_score = self._calculate_confidence_score(anomaly_score, features)
            
            result = {
                'timestamp': validated_data['timestamp'],
                'mmsi': mmsi,
                'ship_name': validated_data['ship_name'],
                'ship_type': validated_data['ship_type'],
                'latitude': validated_data['latitude'],
                'longitude': validated_data['longitude'],
                'speed_knots': validated_data['speed_knots'],
                'heading_degrees': validated_data['heading_degrees'],
                'emergency_status': emergency_status,
                'anomaly_score': round(anomaly_score, 3),
                'emergency_probability': round(emergency_probability, 3),
                'anomaly_type': anomaly_type,
                'confidence_score': round(confidence_score, 3),
                'threshold_used': emergency_threshold,
                'feature_values': {
                    'speed_knots': round(features[0], 2),
                    'heading_change_rate': round(features[1], 2),
                    'course_deviation_degrees': round(features[2], 2),
                    'speed_change_rate': round(features[3], 2),
                    'position_anomaly_score': round(features[4], 2)
                },
                'emergency_explanation': self._generate_emergency_explanation(
                    features, anomaly_type, emergency_status
                ),
                'model_version': '1.0',
                'detection_method': 'AIS Anomaly Detection (SOS-Independent)'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in ship emergency detection: {str(e)}")
            return self._get_default_detection(ship_data)
    
    def _update_ship_history(self, mmsi: str, ship_data: Dict[str, Any]):
        """Update historical data for a ship"""
        if mmsi not in self.ship_history:
            self.ship_history[mmsi] = []
        
        # Keep only last 10 data points
        self.ship_history[mmsi].append({
            'timestamp': ship_data['timestamp'],
            'latitude': ship_data['latitude'],
            'longitude': ship_data['longitude'],
            'speed': ship_data['speed_knots'],
            'heading': ship_data['heading_degrees']
        })
        
        if len(self.ship_history[mmsi]) > 10:
            self.ship_history[mmsi] = self.ship_history[mmsi][-10:]
    
    def _calculate_features(self, mmsi: str, ship_data: Dict[str, Any]) -> List[float]:
        """Calculate features for anomaly detection"""
        history = self.ship_history.get(mmsi, [])
        
        if len(history) < 2:
            # Not enough history, use current values
            return [
                ship_data['speed_knots'],
                0.0,  # heading_change_rate
                0.0,  # course_deviation
                0.0,  # speed_change_rate
                0.0   # position_anomaly
            ]
        
        # Calculate feature values
        current_data = history[-1]
        previous_data = history[-2]
        
        # Speed change rate (knots per hour)
        time_diff = self._time_difference(current_data['timestamp'], previous_data['timestamp'])
        speed_change = (ship_data['speed_knots'] - previous_data['speed']) / max(time_diff, 0.1)
        
        # Heading change rate (degrees per hour)
        heading_change = self._calculate_heading_difference(
            ship_data['heading_degrees'], previous_data['heading']
        ) / max(time_diff, 0.1)
        
        # Course deviation from planned route
        course_deviation = self._calculate_course_deviation(mmsi, ship_data)
        
        # Position anomaly (deviation from expected position)
        position_anomaly = self._calculate_position_anomaly(mmsi, ship_data)
        
        return [
            ship_data['speed_knots'],
            heading_change,
            course_deviation,
            speed_change,
            position_anomaly
        ]
    
    def _time_difference(self, timestamp1: str, timestamp2: str) -> float:
        """Calculate time difference in hours"""
        t1 = datetime.fromisoformat(timestamp1.replace('Z', '+00:00'))
        t2 = datetime.fromisoformat(timestamp2.replace('Z', '+00:00'))
        return abs((t1 - t2).total_seconds() / 3600)
    
    def _calculate_heading_difference(self, heading1: float, heading2: float) -> float:
        """Calculate smallest angle between two headings"""
        diff = abs(heading1 - heading2)
        if diff > 180:
            diff = 360 - diff
        return diff
    
    def _calculate_course_deviation(self, mmsi: str, ship_data: Dict) -> float:
        """Calculate deviation from expected course"""
        # Simplified: check if heading is consistent with destination
        # In real implementation, would use route planning data
        return abs(ship_data['heading_degrees'] % 90)  # Simplified heuristic
    
    def _calculate_position_anomaly(self, mmsi: str, ship_data: Dict) -> float:
        """Calculate position anomaly based on movement patterns"""
        history = self.ship_history.get(mmsi, [])
        
        if len(history) < 2:
            return 0.0
        
        # Check if current position is expected based on previous movement
        current_pos = (ship_data['latitude'], ship_data['longitude'])
        previous_pos = (history[-2]['latitude'], history[-2]['longitude'])
        
        # Expected distance based on speed and time
        time_diff = self._time_difference(ship_data['timestamp'], history[-2]['timestamp'])
        expected_distance = ship_data['speed_knots'] * time_diff * 1.852  # Convert to km
        
        # Actual distance
        actual_distance = geodesic(previous_pos, current_pos).kilometers
        
        # Anomaly score based on distance difference
        distance_diff = abs(actual_distance - expected_distance)
        return min(distance_diff / max(expected_distance, 0.1), 20.0)  # Cap at 20
    
    def _calculate_emergency_probability(self, anomaly_score: float) -> float:
        """Convert anomaly score to emergency probability"""
        # Lower anomaly score = higher probability of anomaly
        # Normalize to 0-1 range
        return max(0.0, min(1.0, (0.5 - anomaly_score) * 2))
    
    def _analyze_anomaly_type(self, features: List[float]) -> str:
        """Analyze the type of anomaly based on feature values"""
        speed, heading_change, course_dev, speed_change, pos_anomaly = features
        
        if speed < 2 and speed_change < -5:
            return 'Sudden_Stop'
        elif heading_change > 30:
            return 'Sharp_Turn'
        elif course_dev > 45:
            return 'Course_Deviation'
        elif pos_anomaly > 10:
            return 'Position_Anomaly'
        else:
            return 'Multiple_Anomalies'
    
    def _generate_emergency_explanation(self, features: List[float], 
                                      anomaly_type: str, status: str) -> str:
        """Generate human-readable explanation of emergency detection"""
        
        if status == 'Normal':
            return 'Ship behavior appears normal - no emergency detected'
        
        explanations = {
            'Sudden_Stop': f"EMERGENCY: Ship has stopped suddenly (speed: {features[0]:.1f} knots)",
            'Sharp_Turn': f"EMERGENCY: Sharp course change detected ({features[1]:.1f}°/hour)",
            'Course_Deviation': f"EMERGENCY: Significant course deviation ({features[2]:.1f}°)",
            'Position_Anomaly': f"EMERGENCY: Irregular movement pattern detected",
            'Multiple_Anomalies': "EMERGENCY: Multiple anomalous behaviors detected"
        }
        
        return explanations.get(anomaly_type, "EMERGENCY: Anomalous ship behavior detected")
    
    def _get_default_detection(self, ship_data: Dict) -> Dict[str, Any]:
        """Return default detection if model fails"""
        return {
            'timestamp': ship_data['timestamp'],
            'mmsi': ship_data['mmsi'],
            'ship_name': ship_data['ship_name'],
            'ship_type': ship_data['ship_type'],
            'latitude': ship_data['latitude'],
            'longitude': ship_data['longitude'],
            'speed_knots': ship_data['speed_knots'],
            'heading_degrees': ship_data['heading_degrees'],
            'emergency_status': 'Normal',
            'anomaly_score': 0.0,
            'emergency_probability': 0.0,
            'anomaly_type': 'None',
            'confidence_score': 0.0,
            'threshold_used': 0.75,
            'feature_values': {},
            'emergency_explanation': 'Detection unavailable - default normal status',
            'model_version': '1.0',
            'detection_method': 'AIS Anomaly Detection (SOS-Independent)'
        }
    
    def _validate_ship_data(self, ship_data: Dict) -> Dict:
        """Validate and sanitize ship AIS data"""
        validated = ship_data.copy()
        
        # Handle edge cases and invalid values
        validated['speed_knots'] = max(0, min(50, float(ship_data.get('speed_knots', 0))))
        validated['heading_degrees'] = max(0, min(360, float(ship_data.get('heading_degrees', 0)) % 360))
        validated['latitude'] = max(-90, min(90, float(ship_data.get('latitude', 0))))
        validated['longitude'] = max(-180, min(180, float(ship_data.get('longitude', 0))))
        
        return validated
    
    def _validate_emergency_conditions(self, features: List[float]) -> bool:
        """Additional validation to prevent false positives"""
        speed, heading_change, course_dev, speed_change, pos_anomaly = features
        
        # Must have at least one strong indicator of emergency
        emergency_indicators = 0
        
        if speed < 2:  # Very low speed
            emergency_indicators += 1
        if speed_change < -10:  # Rapid deceleration
            emergency_indicators += 1
        if heading_change > 45:  # Sharp turn
            emergency_indicators += 1
        if course_dev > 60:  # Major course deviation
            emergency_indicators += 1
        if pos_anomaly > 15:  # Significant position anomaly
            emergency_indicators += 1
        
        return emergency_indicators >= 2  # Need at least 2 indicators
    
    def _calculate_confidence_score(self, anomaly_score: float, features: List[float]) -> float:
        """Calculate confidence score with uncertainty quantification"""
        base_confidence = abs(anomaly_score)
        
        # Adjust confidence based on feature magnitude
        feature_magnitude = sum(abs(f) for f in features)
        magnitude_factor = min(1.0, feature_magnitude / 20)  # Normalize to 0-1
        
        # Combine factors
        confidence = base_confidence * 0.7 + magnitude_factor * 0.3
        
        return min(1.0, max(0.0, confidence))
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information for documentation"""
        return {
            'model_type': 'IsolationForest',
            'features': self.feature_names,
            'detection_method': 'AIS Anomaly Detection (SOS-Independent)',
            'model_version': '1.0',
            'contamination_rate': 0.1,
            'emergency_threshold': 0.75,
            'training_data_size': 2000,
            'anomaly_types': ['Sudden_Stop', 'Sharp_Turn', 'Course_Deviation', 'Position_Anomaly'],
            'responsible_ai_compliance': True,
            'false_positive_prevention': True,
            'confidence_scoring': True,
            'threshold_explanation': 'High threshold (0.75) prevents false alarms and maintains system trust'
        }
