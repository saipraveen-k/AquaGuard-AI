"""
Sample Data Generator for AquaGuard AI MVP
Creates realistic sample datasets for Power BI and demo purposes
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random
import os

def generate_sample_flood_data(num_records: int = 100) -> pd.DataFrame:
    """Generate sample flood prediction data"""
    
    data = []
    base_time = datetime.now() - timedelta(days=7)
    
    locations = [
        {'id': 'LOC001', 'name': 'River Delta Station', 'lat': 40.7128, 'lon': -74.0060},
        {'id': 'LOC002', 'name': 'Coastal Monitoring Point A', 'lat': 34.0522, 'lon': -118.2437},
        {'id': 'LOC003', 'name': 'Harbor Entrance', 'lat': 51.5074, 'lon': -0.1278},
        {'id': 'LOC004', 'name': 'Industrial Port', 'lat': 35.6762, 'lon': 139.6503},
        {'id': 'LOC005', 'name': 'River Basin Station', 'lat': 48.8566, 'lon': 2.3522}
    ]
    
    for i in range(num_records):
        location = random.choice(locations)
        timestamp = base_time + timedelta(hours=i * 2)
        
        # Create realistic patterns with some emergency scenarios
        if i % 20 == 15:  # Emergency scenario every 20 records
            rainfall = random.uniform(25, 50)
            river_level = random.uniform(6, 9)
            soil_moisture = random.uniform(75, 95)
            risk_percentage = random.uniform(75, 95)
            risk_level = 'High'
        elif i % 10 == 5:  # Medium risk scenario
            rainfall = random.uniform(10, 25)
            river_level = random.uniform(4, 6)
            soil_moisture = random.uniform(50, 75)
            risk_percentage = random.uniform(40, 70)
            risk_level = 'Medium'
        else:  # Normal conditions
            rainfall = random.uniform(0, 10)
            river_level = random.uniform(2, 4)
            soil_moisture = random.uniform(20, 50)
            risk_percentage = random.uniform(5, 40)
            risk_level = 'Low'
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'location_id': location['id'],
            'location_name': location['name'],
            'latitude': location['lat'],
            'longitude': location['lon'],
            'rainfall_mm_per_hour': round(rainfall, 2),
            'river_level_meters': round(river_level, 2),
            'soil_moisture_percent': round(soil_moisture, 1),
            'temperature_celsius': round(random.uniform(15, 30), 1),
            'wind_speed_kmh': round(random.uniform(0, 40), 1),
            'atmospheric_pressure_hpa': round(random.uniform(990, 1030), 1),
            'risk_percentage': round(risk_percentage, 2),
            'risk_level': risk_level,
            'time_to_flood_hours': round(random.uniform(1, 24), 1) if risk_level != 'Low' else 999.0,
            'confidence_score': round(random.uniform(0.7, 0.95), 3)
        })
    
    return pd.DataFrame(data)

def generate_sample_ship_data(num_records: int = 200) -> pd.DataFrame:
    """Generate sample ship emergency detection data"""
    
    data = []
    base_time = datetime.now() - timedelta(days=3)
    
    ships = [
        {'mmsi': '000000001', 'name': 'Cargo Voyager', 'type': 'cargo'},
        {'mmsi': '000000002', 'name': 'Ocean Tanker', 'type': 'tanker'},
        {'mmsi': '000000003', 'name': 'Pacific Container', 'type': 'container'},
        {'mmsi': '000000004', 'name': 'Harbor Ferry', 'type': 'passenger'},
        {'mmsi': '000000005', 'name': 'Fishing Pride', 'type': 'fishing'},
        {'mmsi': '000000006', 'name': 'Atlantic Explorer', 'type': 'cargo'},
        {'mmsi': '000000007', 'name': 'Chemical Carrier', 'type': 'tanker'},
        {'mmsi': '000000008', 'name': 'Speed Runner', 'type': 'container'},
        {'mmsi': '000000009', 'name': 'Coast Guardian', 'type': 'passenger'},
        {'mmsi': '000000010', 'name': 'Deep Sea Fisher', 'type': 'fishing'}
    ]
    
    for i in range(num_records):
        ship = random.choice(ships)
        timestamp = base_time + timedelta(minutes=i * 30)
        
        # Create emergency scenarios
        if i % 30 == 25:  # Emergency every 30 records
            speed = random.uniform(0, 5)
            heading = random.uniform(0, 360)
            emergency_status = 'Emergency'
            anomaly_score = random.uniform(-1.0, -0.6)
            emergency_probability = random.uniform(0.8, 1.0)
            anomaly_type = random.choice(['Sudden_Stop', 'Sharp_Turn', 'Course_Deviation'])
        else:  # Normal conditions
            speed = random.uniform(10, 25)
            heading = random.uniform(0, 360)
            emergency_status = 'Normal'
            anomaly_score = random.uniform(-0.5, 0.5)
            emergency_probability = random.uniform(0.0, 0.3)
            anomaly_type = 'None'
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'mmsi': ship['mmsi'],
            'ship_name': ship['name'],
            'ship_type': ship['type'],
            'latitude': round(random.uniform(25, 55), 6),
            'longitude': round(random.uniform(-130, 50), 6),
            'speed_knots': round(speed, 2),
            'heading_degrees': round(heading, 1),
            'destination': random.choice(['New York', 'Los Angeles', 'London', 'Tokyo', 'Singapore']),
            'eta_hours': round(random.uniform(2, 48), 1),
            'status': 'underway' if speed > 0 else 'stopped',
            'emergency_status': emergency_status,
            'anomaly_score': round(anomaly_score, 3),
            'emergency_probability': round(emergency_probability, 3),
            'anomaly_type': anomaly_type,
            'confidence_score': round(random.uniform(0.7, 0.95), 3)
        })
    
    return pd.DataFrame(data)

def generate_sample_spill_data(num_records: int = 50) -> pd.DataFrame:
    """Generate sample oil/chemical spill detection data"""
    
    data = []
    base_time = datetime.now() - timedelta(days=5)
    
    locations = [
        {'id': 'LOC001', 'name': 'River Delta Station', 'lat': 40.7128, 'lon': -74.0060},
        {'id': 'LOC002', 'name': 'Coastal Monitoring Point A', 'lat': 34.0522, 'lon': -118.2437},
        {'id': 'LOC003', 'name': 'Harbor Entrance', 'lat': 51.5074, 'lon': -0.1278},
        {'id': 'LOC004', 'name': 'Industrial Port', 'lat': 35.6762, 'lon': 139.6503}
    ]
    
    for i in range(num_records):
        location = random.choice(locations)
        timestamp = base_time + timedelta(hours=i * 4)
        
        # Create spill scenarios
        if i % 15 == 10:  # Spill detection every 15 records
            spill_detected = True
            spill_type = random.choice(['Oil', 'Chemical'])
            severity = random.choice(['Medium', 'High'])
            confidence = random.uniform(0.7, 0.95)
            affected_area = random.uniform(0.5, 5.0)
        else:  # No spill
            spill_detected = False
            spill_type = 'None'
            severity = 'Low'
            confidence = random.uniform(0.8, 0.95)
            affected_area = 0.0
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'location_id': location['id'],
            'location_name': location['name'],
            'latitude': location['lat'] + random.uniform(-0.1, 0.1),
            'longitude': location['lon'] + random.uniform(-0.1, 0.1),
            'spill_detected': spill_detected,
            'spill_type': spill_type,
            'severity_level': severity,
            'affected_area_km2': round(affected_area, 3),
            'confidence_score': round(confidence, 3),
            'source_type': random.choice(['ship', 'platform', 'pipeline', 'unknown']),
            'estimated_volume_liters': random.choice([0, 100, 500, 1000, 5000, 10000]) if spill_detected else 0,
            'weather_wind_speed_kmh': round(random.uniform(0, 30), 1),
            'weather_wave_height_meters': round(random.uniform(0.5, 3.0), 1)
        })
    
    return pd.DataFrame(data)

def generate_sample_alerts(num_records: int = 30) -> pd.DataFrame:
    """Generate sample alert data"""
    
    data = []
    base_time = datetime.now() - timedelta(days=2)
    
    alert_types = ['Flood', 'Ship Emergency', 'Oil Spill']
    alert_levels = ['Low', 'Medium', 'High', 'Critical']
    
    for i in range(num_records):
        timestamp = base_time + timedelta(hours=i * 2)
        alert_type = random.choice(alert_types)
        alert_level = random.choice(alert_levels)
        
        # Generate appropriate messages
        if alert_type == 'Flood':
            title = f"Flood Risk Alert - Station {random.choice(['A', 'B', 'C'])}"
            message = f"Flood risk {random.randint(60, 95)}%. Expected flooding in {random.randint(2, 12)} hours."
        elif alert_type == 'Ship Emergency':
            title = f"Ship Emergency - {random.choice(['Cargo Voyager', 'Ocean Tanker', 'Pacific Container'])}"
            message = "Vessel showing anomalous behavior. Immediate response required."
        else:  # Oil Spill
            title = f"{random.choice(['Oil', 'Chemical'])} Spill Detected"
            message = f"Spill detected affecting {random.uniform(0.5, 3.0):.1f} km². Deploy containment team."
        
        data.append({
            'alert_id': f"ALT-{i+1:03d}",
            'timestamp': timestamp.isoformat(),
            'alert_type': alert_type,
            'level': alert_level,
            'title': title,
            'message': message,
            'status': random.choice(['active', 'acknowledged']),
            'latitude': round(random.uniform(25, 55), 6),
            'longitude': round(random.uniform(-130, 50), 6),
            'location_name': random.choice(['River Delta', 'Coastal Point', 'Harbor Entrance', 'Industrial Port']),
            'actions_required': random.randint(1, 5),
            'priority_score': {'Low': 4, 'Medium': 3, 'High': 2, 'Critical': 1}[alert_level]
        })
    
    return pd.DataFrame(data)

def generate_sample_digital_twin() -> pd.DataFrame:
    """Generate sample digital twin simulation data"""
    
    data = []
    base_time = datetime.now() - timedelta(hours=6)
    
    for i in range(13):  # 6 hours of data, every 30 minutes
        timestamp = base_time + timedelta(minutes=i * 30)
        
        # Simulate evolving conditions
        flood_area = 2.0 + (i * 0.3) + random.uniform(-0.2, 0.2)
        spill_area = 1.0 + (i * 0.15) + random.uniform(-0.1, 0.1)
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'flooded_area_km2': round(max(0, flood_area), 3),
            'spilled_area_km2': round(max(0, spill_area), 3),
            'max_flood_depth': round(random.uniform(0.5, 2.5), 2),
            'max_spill_concentration': round(random.uniform(0.3, 0.9), 2),
            'overall_risk_score': round(min(1.0, 0.3 + (i * 0.05) + random.uniform(-0.1, 0.1)), 3),
            'risk_level': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'wind_speed_kmh': round(random.uniform(5, 25), 1),
            'wind_direction_degrees': round(random.uniform(0, 360), 1),
            'water_current_speed_kmh': round(random.uniform(1, 5), 1),
            'simulation_type': 'Digital Twin Simulation (MVP Concept)'
        })
    
    return pd.DataFrame(data)

def create_all_sample_datasets():
    """Create all sample datasets and save to CSV files"""
    
    # Create output directory
    output_dir = "./data/outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate and save all datasets
    datasets = {
        'flood_predictions': generate_sample_flood_data(),
        'ship_emergencies': generate_sample_ship_data(),
        'spill_detections': generate_sample_spill_data(),
        'alerts': generate_sample_alerts(),
        'digital_twin': generate_sample_digital_twin()
    }
    
    for name, df in datasets.items():
        file_path = f"{output_dir}/{name}.csv"
        df.to_csv(file_path, index=False)
        print(f"Created {file_path} with {len(df)} records")
    
    # Create data schemas documentation
    create_data_schemas_documentation()
    
    print(f"\nAll sample datasets created in {output_dir}")
    return datasets

def create_data_schemas_documentation():
    """Create comprehensive data schemas documentation"""
    
    schemas = {
        'flood_predictions': {
            'description': 'Flood risk prediction results from Azure ML model',
            'columns': [
                {'name': 'timestamp', 'type': 'datetime', 'description': 'Prediction timestamp', 'example': '2024-01-15T10:30:00'},
                {'name': 'location_id', 'type': 'string', 'description': 'Unique location identifier', 'example': 'LOC001'},
                {'name': 'location_name', 'type': 'string', 'description': 'Human-readable location name', 'example': 'River Delta Station'},
                {'name': 'latitude', 'type': 'float', 'description': 'Location latitude', 'example': '40.7128'},
                {'name': 'longitude', 'type': 'float', 'description': 'Location longitude', 'example': '-74.0060'},
                {'name': 'rainfall_mm_per_hour', 'type': 'float', 'description': 'Current rainfall rate', 'example': '25.5'},
                {'name': 'river_level_meters', 'type': 'float', 'description': 'River water level', 'example': '6.2'},
                {'name': 'soil_moisture_percent', 'type': 'float', 'description': 'Soil moisture content', 'example': '78.5'},
                {'name': 'risk_percentage', 'type': 'float', 'description': 'Flood risk probability (0-100)', 'example': '85.2'},
                {'name': 'risk_level', 'type': 'string', 'description': 'Risk categorization', 'example': 'High'},
                {'name': 'time_to_flood_hours', 'type': 'float', 'description': 'Estimated time to flooding', 'example': '4.5'},
                {'name': 'confidence_score', 'type': 'float', 'description': 'Model confidence (0-1)', 'example': '0.923'}
            ]
        },
        'ship_emergencies': {
            'description': 'Ship emergency detection results from AIS analysis',
            'columns': [
                {'name': 'timestamp', 'type': 'datetime', 'description': 'Detection timestamp', 'example': '2024-01-15T10:30:00'},
                {'name': 'mmsi', 'type': 'string', 'description': 'Maritime Mobile Service Identity', 'example': '000000001'},
                {'name': 'ship_name', 'type': 'string', 'description': 'Vessel name', 'example': 'Cargo Voyager'},
                {'name': 'ship_type', 'type': 'string', 'description': 'Vessel category', 'example': 'cargo'},
                {'name': 'latitude', 'type': 'float', 'description': 'Current latitude', 'example': '40.7128'},
                {'name': 'longitude', 'type': 'float', 'description': 'Current longitude', 'example': '-74.0060'},
                {'name': 'speed_knots', 'type': 'float', 'description': 'Current speed', 'example': '12.5'},
                {'name': 'heading_degrees', 'type': 'float', 'description': 'Course heading', 'example': '045.0'},
                {'name': 'emergency_status', 'type': 'string', 'description': 'Emergency detection result', 'example': 'Emergency'},
                {'name': 'anomaly_score', 'type': 'float', 'description': 'Anomaly detection score', 'example': '-0.85'},
                {'name': 'emergency_probability', 'type': 'float', 'description': 'Emergency probability (0-1)', 'example': '0.92'},
                {'name': 'anomaly_type', 'type': 'string', 'description': 'Type of anomaly detected', 'example': 'Sudden_Stop'}
            ]
        },
        'spill_detections': {
            'description': 'Oil and chemical spill detection from image analysis',
            'columns': [
                {'name': 'timestamp', 'type': 'datetime', 'description': 'Detection timestamp', 'example': '2024-01-15T10:30:00'},
                {'name': 'location_id', 'type': 'string', 'description': 'Unique location identifier', 'example': 'LOC001'},
                {'name': 'location_name', 'type': 'string', 'description': 'Human-readable location name', 'example': 'River Delta Station'},
                {'name': 'latitude', 'type': 'float', 'description': 'Spill location latitude', 'example': '40.7128'},
                {'name': 'longitude', 'type': 'float', 'description': 'Spill location longitude', 'example': '-74.0060'},
                {'name': 'spill_detected', 'type': 'boolean', 'description': 'Whether spill was detected', 'example': 'True'},
                {'name': 'spill_type', 'type': 'string', 'description': 'Type of spill', 'example': 'Oil'},
                {'name': 'severity_level', 'type': 'string', 'description': 'Spill severity', 'example': 'High'},
                {'name': 'affected_area_km2', 'type': 'float', 'description': 'Estimated affected area', 'example': '2.35'},
                {'name': 'confidence_score', 'type': 'float', 'description': 'Detection confidence (0-1)', 'example': '0.89'},
                {'name': 'source_type', 'type': 'string', 'description': 'Likely spill source', 'example': 'ship'},
                {'name': 'estimated_volume_liters', 'type': 'integer', 'description': 'Estimated spill volume', 'example': '5000'}
            ]
        },
        'alerts': {
            'description': 'System alerts generated from all detection modules',
            'columns': [
                {'name': 'alert_id', 'type': 'string', 'description': 'Unique alert identifier', 'example': 'ALT-001'},
                {'name': 'timestamp', 'type': 'datetime', 'description': 'Alert generation time', 'example': '2024-01-15T10:30:00'},
                {'name': 'alert_type', 'type': 'string', 'description': 'Type of alert', 'example': 'Flood'},
                {'name': 'level', 'type': 'string', 'description': 'Alert severity level', 'example': 'High'},
                {'name': 'title', 'type': 'string', 'description': 'Alert title', 'example': 'Flood Risk Alert - Station A'},
                {'name': 'message', 'type': 'string', 'description': 'Detailed alert message', 'example': 'Flood risk 85%. Expected flooding in 4.5 hours.'},
                {'name': 'status', 'type': 'string', 'description': 'Alert status', 'example': 'active'},
                {'name': 'latitude', 'type': 'float', 'description': 'Alert location latitude', 'example': '40.7128'},
                {'name': 'longitude', 'type': 'float', 'description': 'Alert location longitude', 'example': '-74.0060'},
                {'name': 'location_name', 'type': 'string', 'description': 'Alert location name', 'example': 'River Delta'},
                {'name': 'actions_required', 'type': 'integer', 'description': 'Number of recommended actions', 'example': '3'},
                {'name': 'priority_score', 'type': 'integer', 'description': 'Priority for sorting (1=highest)', 'example': '2'}
            ]
        },
        'digital_twin': {
            'description': 'Digital twin simulation state and predictions',
            'columns': [
                {'name': 'timestamp', 'type': 'datetime', 'description': 'Simulation timestamp', 'example': '2024-01-15T10:30:00'},
                {'name': 'flooded_area_km2', 'type': 'float', 'description': 'Simulated flooded area', 'example': '3.5'},
                {'name': 'spilled_area_km2', 'type': 'float', 'description': 'Simulated spill area', 'example': '1.8'},
                {'name': 'max_flood_depth', 'type': 'float', 'description': 'Maximum flood depth', 'example': '1.2'},
                {'name': 'max_spill_concentration', 'type': 'float', 'description': 'Maximum spill concentration', 'example': '0.75'},
                {'name': 'overall_risk_score', 'type': 'float', 'description': 'Overall risk assessment (0-1)', 'example': '0.68'},
                {'name': 'risk_level', 'type': 'string', 'description': 'Overall risk level', 'example': 'Medium'},
                {'name': 'wind_speed_kmh', 'type': 'float', 'description': 'Wind speed for simulation', 'example': '15.2'},
                {'name': 'wind_direction_degrees', 'type': 'float', 'description': 'Wind direction', 'example': '045.0'},
                {'name': 'water_current_speed_kmh', 'type': 'float', 'description': 'Water current speed', 'example': '2.8'},
                {'name': 'simulation_type', 'type': 'string', 'description': 'Simulation type identifier', 'example': 'Digital Twin Simulation (MVP Concept)'}
            ]
        }
    }
    
    # Save schemas as JSON
    schemas_path = "./data/outputs/data_schemas.json"
    with open(schemas_path, 'w') as f:
        json.dump(schemas, f, indent=2)
    
    print(f"Data schemas documentation created: {schemas_path}")
    return schemas

if __name__ == "__main__":
    create_all_sample_datasets()
