"""
Data Generator Module for AquaGuard AI
Simulates realistic environmental and maritime data for MVP demo
"""

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import faker
from geopy.distance import geodesic
import logging

logger = logging.getLogger(__name__)

class DataSimulator:
    """Generates simulated data for all AquaGuard AI modules"""
    
    def __init__(self):
        self.fake = faker.Faker()
        self.locations = self._initialize_locations()
        self.ships = self._initialize_ships()
        
    def _initialize_locations(self) -> List[Dict]:
        """Initialize monitoring locations (flood zones, coastal areas)"""
        return [
            {'id': 'LOC001', 'name': 'River Delta Station', 'lat': 40.7128, 'lon': -74.0060, 'type': 'river'},
            {'id': 'LOC002', 'name': 'Coastal Monitoring Point A', 'lat': 34.0522, 'lon': -118.2437, 'type': 'coastal'},
            {'id': 'LOC003', 'name': 'Harbor Entrance', 'lat': 51.5074, 'lon': -0.1278, 'type': 'harbor'},
            {'id': 'LOC004', 'name': 'Industrial Port', 'lat': 35.6762, 'lon': 139.6503, 'type': 'port'},
            {'id': 'LOC005', 'name': 'River Basin Station', 'lat': 48.8566, 'lon': 2.3522, 'type': 'river'},
        ]
    
    def _initialize_ships(self) -> List[Dict]:
        """Initialize ship fleet for monitoring"""
        ships = []
        ship_types = ['cargo', 'tanker', 'container', 'passenger', 'fishing']
        
        for i in range(10):
            ship = {
                'mmsi': f"0000{i:06d}",  # Maritime Mobile Service Identity
                'name': f"Ship_{i+1}",
                'type': random.choice(ship_types),
                'length': random.uniform(50, 300),
                'current_lat': random.uniform(25, 55),
                'current_lon': random.uniform(-130, 50),
                'speed': random.uniform(10, 25),
                'heading': random.uniform(0, 360),
                'destination': random.choice(self.locations)['name']
            }
            ships.append(ship)
        
        return ships
    
    def generate_flood_data(self, num_points: int = 5) -> List[Dict]:
        """Generate flood monitoring data with realistic patterns"""
        data = []
        current_time = datetime.now()
        
        for i in range(num_points):
            location = self.locations[i % len(self.locations)]
            
            # Simulate weather patterns (can create flood conditions)
            base_rainfall = random.uniform(0, 50)  # mm per hour
            if random.random() < 0.2:  # 20% chance of heavy rain
                base_rainfall *= random.uniform(2, 5)
            
            # River level responds to rainfall with delay
            river_level = random.uniform(2.0, 8.0) + (base_rainfall * 0.1)
            
            # Soil moisture increases with rain
            soil_moisture = min(95, random.uniform(30, 70) + (base_rainfall * 0.5))
            
            data_point = {
                'timestamp': current_time.isoformat(),
                'location_id': location['id'],
                'location_name': location['name'],
                'latitude': location['lat'],
                'longitude': location['lon'],
                'rainfall_mm_per_hour': round(base_rainfall, 2),
                'river_level_meters': round(river_level, 2),
                'soil_moisture_percent': round(soil_moisture, 1),
                'temperature_celsius': round(random.uniform(15, 30), 1),
                'wind_speed_kmh': round(random.uniform(0, 40), 1),
                'atmospheric_pressure_hpa': round(random.uniform(990, 1030), 1)
            }
            
            data.append(data_point)
        
        return data
    
    def generate_ship_data(self, num_ships: int = 10) -> List[Dict]:
        """Generate AIS-like ship tracking data"""
        data = []
        current_time = datetime.now()
        
        for i, ship in enumerate(self.ships[:num_ships]):
            # Simulate ship movement
            if random.random() < 0.1:  # 10% chance of emergency behavior
                # Emergency: sudden speed drop or course deviation
                speed_change = random.uniform(-15, -5)
                course_change = random.uniform(-45, 45)
            else:
                # Normal movement
                speed_change = random.uniform(-2, 2)
                course_change = random.uniform(-5, 5)
            
            new_speed = max(0, ship['speed'] + speed_change)
            new_heading = (ship['heading'] + course_change) % 360
            
            # Update position based on speed and heading
            distance_km = (ship['speed'] / 3600) * 1.852  # Convert knots to km
            new_lat = ship['current_lat'] + (distance_km * np.cos(np.radians(new_heading))) / 111
            new_lon = ship['current_lon'] + (distance_km * np.sin(np.radians(new_heading))) / (111 * np.cos(np.radians(ship['current_lat'])))
            
            # Update ship state
            ship['current_lat'] = new_lat
            ship['current_lon'] = new_lon
            ship['speed'] = new_speed
            ship['heading'] = new_heading
            
            data_point = {
                'timestamp': current_time.isoformat(),
                'mmsi': ship['mmsi'],
                'ship_name': ship['name'],
                'ship_type': ship['type'],
                'latitude': round(new_lat, 6),
                'longitude': round(new_lon, 6),
                'speed_knots': round(new_speed, 2),
                'heading_degrees': round(new_heading, 1),
                'destination': ship['destination'],
                'eta_hours': round(random.uniform(2, 48), 1),
                'status': 'underway' if new_speed > 0 else 'stopped'
            }
            
            data.append(data_point)
        
        return data
    
    def generate_spill_scenarios(self, num_scenarios: int = 3) -> List[Tuple[str, Dict]]:
        """Generate oil/chemical spill scenarios with metadata"""
        scenarios = []
        current_time = datetime.now()
        
        for i in range(num_scenarios):
            location = random.choice(self.locations)
            
            # Create spill metadata
            metadata = {
                'timestamp': current_time.isoformat(),
                'location_id': location['id'],
                'location_name': location['name'],
                'latitude': location['lat'] + random.uniform(-0.1, 0.1),
                'longitude': location['lon'] + random.uniform(-0.1, 0.1),
                'spill_type': random.choice(['oil', 'chemical', 'unknown']),
                'source_type': random.choice(['ship', 'platform', 'pipeline', 'unknown']),
                'estimated_volume_liters': random.choice([100, 500, 1000, 5000, 10000]),
                'weather_conditions': {
                    'wind_speed_kmh': random.uniform(0, 30),
                    'wave_height_meters': random.uniform(0.5, 3.0),
                    'visibility_km': random.uniform(1, 10)
                }
            }
            
            # For MVP, we'll use placeholder images
            # In real implementation, these would be satellite/drone images
            image_path = f"./data/images/spill_scenario_{i+1}.jpg"
            
            scenarios.append((image_path, metadata))
        
        return scenarios
    
    def generate_emergency_scenario(self) -> Dict:
        """Generate a specific emergency scenario for demo purposes"""
        scenario_type = random.choice(['flood', 'ship_emergency', 'oil_spill'])
        
        if scenario_type == 'flood':
            return {
                'type': 'flood',
                'severity': 'high',
                'location': random.choice(self.locations),
                'description': 'Heavy rainfall causing rapid river level rise',
                'affected_area_km2': random.uniform(10, 100)
            }
        elif scenario_type == 'ship_emergency':
            return {
                'type': 'ship_emergency',
                'severity': 'medium',
                'ship': random.choice(self.ships),
                'description': 'Vessel experiencing engine failure',
                'coordinates': {
                    'lat': random.choice(self.ships)['current_lat'],
                    'lon': random.choice(self.ships)['current_lon']
                }
            }
        else:  # oil_spill
            return {
                'type': 'oil_spill',
                'severity': 'high',
                'location': random.choice(self.locations),
                'description': 'Oil spill detected near industrial port',
                'estimated_volume': random.uniform(1000, 10000),
                'coordinates': {
                    'lat': random.choice(self.locations)['lat'],
                    'lon': random.choice(self.locations)['lon']
                }
            }
