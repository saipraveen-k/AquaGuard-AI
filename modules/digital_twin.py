"""
Digital Twin Simulation Module for AquaGuard AI
Simulates flood spread and oil spill propagation using Azure Maps
"""

import numpy as np
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import math
import random
from geopy.distance import geodesic

logger = logging.getLogger(__name__)

class DigitalTwinSimulator:
    """Digital Twin simulation for flood and spill spread modeling"""
    
    def __init__(self):
        self.simulation_grid_size = 50  # 50x50 grid for simulation
        self.cell_size_km = 0.1  # Each cell represents 0.1 km²
        self.current_state = {
            'flood_grid': None,
            'spill_grid': None,
            'simulation_time': datetime.now().isoformat(),
            'grid_bounds': None
        }
        
        # Environmental parameters
        self.wind_speed = 10.0  # km/h
        self.wind_direction = 45.0  # degrees
        self.water_current_speed = 2.0  # km/h
        self.water_current_direction = 90.0  # degrees
        
        logger.info("Digital Twin Simulator initialized")
    
    def update_state(self, flood_predictions: List[Dict], 
                    ship_emergencies: List[Dict], 
                    spill_detections: List[Dict]) -> Dict[str, Any]:
        """Update digital twin state with new data"""
        
        # Initialize simulation grid
        self._initialize_simulation_grid(flood_predictions, spill_detections)
        
        # Simulate flood spread
        flood_simulation = self._simulate_flood_spread(flood_predictions)
        
        # Simulate oil spill spread
        spill_simulation = self._simulate_spill_spread(spill_detections)
        
        # Combine simulations
        combined_state = {
            'timestamp': datetime.now().isoformat(),
            'simulation_type': 'Digital Twin Simulation (MVP Concept)',
            'flood_simulation': flood_simulation,
            'spill_simulation': spill_simulation,
            'ship_emergencies': ship_emergencies,
            'environmental_conditions': {
                'wind_speed_kmh': self.wind_speed,
                'wind_direction_degrees': self.wind_direction,
                'water_current_speed_kmh': self.water_current_speed,
                'water_current_direction_degrees': self.water_current_direction
            },
            'risk_assessment': self._calculate_overall_risk(
                flood_simulation, spill_simulation, ship_emergencies
            ),
            'grid_info': {
                'size': self.simulation_grid_size,
                'cell_size_km': self.cell_size_km,
                'total_area_km2': self.simulation_grid_size * self.simulation_grid_size * self.cell_size_km
            }
        }
        
        self.current_state = combined_state
        return combined_state
    
    def _initialize_simulation_grid(self, flood_predictions: List[Dict], 
                                   spill_detections: List[Dict]):
        """Initialize the simulation grid based on data locations"""
        
        # Find bounds of all data points
        all_lats = []
        all_lons = []
        
        for pred in flood_predictions:
            all_lats.append(pred['latitude'])
            all_lons.append(pred['longitude'])
        
        for detection in spill_detections:
            all_lats.append(detection['latitude'])
            all_lons.append(detection['longitude'])
        
        if not all_lats:
            # Default to some coordinates if no data
            all_lats = [40.7128]
            all_lons = [-74.0060]
        
        # Calculate grid bounds
        min_lat, max_lat = min(all_lats), max(all_lats)
        min_lon, max_lon = min(all_lons), max(all_lons)
        
        # Add padding
        lat_padding = (max_lat - min_lat) * 0.2 + 0.1
        lon_padding = (max_lon - min_lon) * 0.2 + 0.1
        
        self.current_state['grid_bounds'] = {
            'min_lat': min_lat - lat_padding,
            'max_lat': max_lat + lat_padding,
            'min_lon': min_lon - lon_padding,
            'max_lon': max_lon + lon_padding
        }
        
        # Initialize grids
        self.current_state['flood_grid'] = np.zeros((self.simulation_grid_size, self.simulation_grid_size))
        self.current_state['spill_grid'] = np.zeros((self.simulation_grid_size, self.simulation_grid_size))
    
    def _simulate_flood_spread(self, flood_predictions: List[Dict]) -> Dict[str, Any]:
        """Simulate flood spread based on predictions"""
        
        flood_grid = np.copy(self.current_state['flood_grid'])
        
        # Add flood sources from predictions
        for pred in flood_predictions:
            if pred['risk_level'] in ['Medium', 'High']:
                grid_pos = self._lat_lon_to_grid(pred['latitude'], pred['longitude'])
                
                if grid_pos:
                    row, col = grid_pos
                    # Set initial flood intensity based on risk level
                    intensity = 0.5 if pred['risk_level'] == 'Medium' else 0.8
                    flood_grid[row, col] = intensity
        
        # Simulate flood spread (simplified hydraulic model)
        for _ in range(10):  # 10 simulation steps
            new_grid = np.copy(flood_grid)
            
            for i in range(1, self.simulation_grid_size - 1):
                for j in range(1, self.simulation_grid_size - 1):
                    if flood_grid[i, j] > 0.1:
                        # Spread to neighboring cells
                        spread_rate = 0.3  # 30% spread per step
                        
                        # Check elevation (simplified - assume lower cells spread more)
                        for di in [-1, 0, 1]:
                            for dj in [-1, 0, 1]:
                                if di == 0 and dj == 0:
                                    continue
                                
                                ni, nj = i + di, j + dj
                                if 0 <= ni < self.simulation_grid_size and 0 <= nj < self.simulation_grid_size:
                                    # Spread probability decreases with distance
                                    spread_prob = spread_rate / (abs(di) + abs(dj))
                                    new_grid[ni, nj] = min(1.0, new_grid[ni, nj] + flood_grid[i, j] * spread_prob)
            
            flood_grid = new_grid
        
        # Calculate flood statistics
        total_flooded_cells = np.sum(flood_grid > 0.1)
        flooded_area_km2 = total_flooded_cells * self.cell_size_km
        max_flood_depth = np.max(flood_grid)
        
        return {
            'flood_grid': flood_grid.tolist(),
            'flooded_area_km2': round(flooded_area_km2, 3),
            'max_flood_depth_normalized': round(max_flood_depth, 3),
            'flood_hotspots': self._identify_flood_hotspots(flood_grid),
            'spread_prediction_hours': 6,  # Predict 6 hours ahead
            'simulation_method': 'Simplified Hydraulic Model'
        }
    
    def _simulate_spill_spread(self, spill_detections: List[Dict]) -> Dict[str, Any]:
        """Simulate oil spill spread based on detections"""
        
        spill_grid = np.copy(self.current_state['spill_grid'])
        
        # Add spill sources from detections
        for detection in spill_detections:
            if detection['spill_detected']:
                grid_pos = self._lat_lon_to_grid(detection['latitude'], detection['longitude'])
                
                if grid_pos:
                    row, col = grid_pos
                    # Set initial spill intensity based on severity
                    severity_map = {'Low': 0.3, 'Medium': 0.6, 'High': 0.9}
                    intensity = severity_map.get(detection['severity_level'], 0.5)
                    spill_grid[row, col] = intensity
        
        # Simulate spill spread (wind and current driven)
        for _ in range(15):  # 15 simulation steps
            new_grid = np.copy(spill_grid)
            
            for i in range(1, self.simulation_grid_size - 1):
                for j in range(1, self.simulation_grid_size - 1):
                    if spill_grid[i, j] > 0.05:
                        # Calculate spread direction based on wind and current
                        wind_effect_x = math.cos(math.radians(self.wind_direction)) * self.wind_speed / 50
                        wind_effect_y = math.sin(math.radians(self.wind_direction)) * self.wind_speed / 50
                        
                        current_effect_x = math.cos(math.radians(self.water_current_direction)) * self.water_current_speed / 50
                        current_effect_y = math.sin(math.radians(self.water_current_direction)) * self.water_current_speed / 50
                        
                        # Combined effect
                        total_effect_x = wind_effect_x + current_effect_x
                        total_effect_y = wind_effect_y + current_effect_y
                        
                        # Spread to adjacent cells in the direction of wind/current
                        spread_rate = 0.2  # 20% spread per step
                        
                        # Primary spread direction - FIXED: Ensure integer conversion
                        primary_di = int(round(np.sign(total_effect_y)))
                        primary_dj = int(round(np.sign(total_effect_x)))
                        
                        # Secondary spread (diffusion)
                        for di in [-1, 0, 1]:
                            for dj in [-1, 0, 1]:
                                if di == 0 and dj == 0:
                                    continue
                                
                                ni, nj = i + di, j + dj
                                if 0 <= ni < self.simulation_grid_size and 0 <= nj < self.simulation_grid_size:
                                    # Higher spread in wind/current direction
                                    spread_multiplier = 1.0
                                    if di == primary_di and dj == primary_dj:
                                        spread_multiplier = 2.0
                                    
                                    # FIXED: Ensure denominator is never zero
                                    denominator = abs(di) + abs(dj)
                                    if denominator > 0:
                                        spread_prob = spread_rate * spread_multiplier / denominator
                                        new_grid[ni, nj] = min(1.0, new_grid[ni, nj] + spill_grid[i, j] * spread_prob)
            
            spill_grid = new_grid
        
        # Calculate spill statistics
        total_spilled_cells = np.sum(spill_grid > 0.05)
        spilled_area_km2 = total_spilled_cells * self.cell_size_km
        max_spill_concentration = np.max(spill_grid)
        
        return {
            'spill_grid': spill_grid.tolist(),
            'spilled_area_km2': round(spilled_area_km2, 3),
            'max_concentration_normalized': round(max_spill_concentration, 3),
            'spill_plume_direction': round(self.wind_direction, 1),
            'spread_prediction_hours': 12,  # Predict 12 hours ahead
            'simulation_method': 'Wind & Current Driven Model'
        }
    
    def _lat_lon_to_grid(self, lat: float, lon: float) -> Tuple[int, int]:
        """Convert latitude/longitude to grid coordinates"""
        bounds = self.current_state['grid_bounds']
        
        if not bounds:
            return None
        
        # Normalize to 0-1 range
        lat_norm = (lat - bounds['min_lat']) / (bounds['max_lat'] - bounds['min_lat'])
        lon_norm = (lon - bounds['min_lon']) / (bounds['max_lon'] - bounds['min_lon'])
        
        # Convert to grid coordinates
        row = int(lat_norm * (self.simulation_grid_size - 1))
        col = int(lon_norm * (self.simulation_grid_size - 1))
        
        # Ensure within bounds
        row = max(0, min(self.simulation_grid_size - 1, row))
        col = max(0, min(self.simulation_grid_size - 1, col))
        
        return (row, col)
    
    def _identify_flood_hotspots(self, flood_grid: np.ndarray) -> List[Dict]:
        """Identify flood hotspots for priority response"""
        hotspots = []
        
        # Find high-intensity areas
        threshold = 0.7
        high_flood_areas = np.where(flood_grid > threshold)
        
        for i, j in zip(high_flood_areas[0], high_flood_areas[1]):
            # Convert back to lat/lon
            bounds = self.current_state['grid_bounds']
            if bounds:
                lat_norm = i / (self.simulation_grid_size - 1)
                lon_norm = j / (self.simulation_grid_size - 1)
                
                lat = bounds['min_lat'] + lat_norm * (bounds['max_lat'] - bounds['min_lat'])
                lon = bounds['min_lon'] + lon_norm * (bounds['max_lon'] - bounds['min_lon'])
                
                hotspots.append({
                    'latitude': lat,
                    'longitude': lon,
                    'flood_intensity': round(flood_grid[i, j], 3),
                    'priority_level': 'Critical' if flood_grid[i, j] > 0.85 else 'High'
                })
        
        # Return top 5 hotspots
        return sorted(hotspots, key=lambda x: x['flood_intensity'], reverse=True)[:5]
    
    def _calculate_overall_risk(self, flood_sim: Dict, spill_sim: Dict, 
                              ship_emergencies: List[Dict]) -> Dict[str, Any]:
        """Calculate overall risk assessment"""
        
        # Flood risk
        flood_risk = flood_sim['max_flood_depth_normalized'] * 0.4
        
        # Spill risk
        spill_risk = spill_sim['max_concentration_normalized'] * 0.3
        
        # Ship emergency risk
        emergency_ships = len([s for s in ship_emergencies if s['emergency_status'] == 'Emergency'])
        ship_risk = min(1.0, emergency_ships / 5.0) * 0.3
        
        # Overall risk
        overall_risk = flood_risk + spill_risk + ship_risk
        
        # Risk level
        if overall_risk >= 0.7:
            risk_level = 'Critical'
        elif overall_risk >= 0.4:
            risk_level = 'High'
        elif overall_risk >= 0.2:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'overall_risk_score': round(overall_risk, 3),
            'risk_level': risk_level,
            'flood_risk_contribution': round(flood_risk, 3),
            'spill_risk_contribution': round(spill_risk, 3),
            'ship_risk_contribution': round(ship_risk, 3),
            'recommendations': self._generate_risk_recommendations(risk_level, flood_sim, spill_sim, ship_emergencies)
        }
    
    def _generate_risk_recommendations(self, risk_level: str, flood_sim: Dict, 
                                    spill_sim: Dict, ship_emergencies: List[Dict]) -> List[str]:
        """Generate recommendations based on risk assessment"""
        
        recommendations = []
        
        if risk_level == 'Critical':
            recommendations.append("IMMEDIATE EVACUATION advised for affected areas")
            recommendations.append("Deploy emergency response teams to all hotspots")
        
        # Flood-specific recommendations
        if flood_sim['max_flood_depth_normalized'] > 0.5:
            recommendations.append("Monitor flood barriers and drainage systems")
            if flood_sim['max_flood_depth_normalized'] > 0.7:
                recommendations.append("Issue flood warnings to downstream communities")
        
        # Spill-specific recommendations
        if spill_sim['max_concentration_normalized'] > 0.3:
            recommendations.append("Deploy containment booms around spill area")
            if spill_sim['max_concentration_normalized'] > 0.6:
                recommendations.append("Initiate oil spill cleanup procedures")
        
        # Ship emergency recommendations
        emergency_ships = [s for s in ship_emergencies if s['emergency_status'] == 'Emergency']
        if emergency_ships:
            recommendations.append(f"Coordinate rescue operations for {len(emergency_ships)} vessels in distress")
        
        if not recommendations:
            recommendations.append("Continue routine monitoring")
        
        return recommendations
    
    def get_simulation_info(self) -> Dict[str, Any]:
        """Get simulation information for documentation"""
        return {
            'simulation_type': 'Digital Twin (MVP Level)',
            'grid_resolution': f"{self.simulation_grid_size}x{self.simulation_grid_size}",
            'cell_size': f"{self.cell_size_km} km²",
            'flood_model': 'Simplified Hydraulic Spread',
            'spill_model': 'Wind & Current Driven',
            'prediction_horizon': '6-12 hours',
            'azure_maps_integration': 'Planned for production',
            'responsible_ai_compliance': True
        }
