"""
AquaGuard AI - Unified Flood, Ocean & Maritime Emergency Intelligence System
Main Orchestrator for Imagine Cup MVP

This module coordinates all AI modules and manages data flow for demo.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import asyncio
import pandas as pd
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AquaGuardAI:
    """Main orchestrator for AquaGuard AI system"""
    
    def __init__(self):
        # Initialize data storage
        self.current_data = {
            'flood_data': [],
            'ship_data': [],
            'spill_data': [],
            'alerts': []
        }
        
    def generate_flood_data(self):
        """Generate realistic flood prediction data"""
        locations = ['Tokyo Bay', 'Yokohama Port', 'Shibuya', 'Shinagawa', 'Chiba Coast']
        data = []
        for i in range(10):
            data.append({
                'location': locations[i % len(locations)],
                'timestamp': datetime.now().isoformat(),
                'rainfall_mm': round(random.uniform(5, 50), 1),
                'river_level_m': round(random.uniform(1, 5), 1),
                'soil_moisture': round(random.uniform(20, 80), 1),
                'risk_percentage': round(random.uniform(5, 25), 1),
                'time_to_flood_hours': round(random.uniform(6, 24), 1),
                'confidence_score': round(random.uniform(85, 95), 1)
            })
        return data
    
    def generate_ship_data(self):
        """Generate realistic ship emergency data"""
        ships = ['Cargo Vessel Alpha', 'Tanker Beta', 'Container Ship Gamma']
        data = []
        for i in range(5):
            data.append({
                'ship_id': f'SHIP-{1000+i}',
                'ship_name': ships[i % len(ships)],
                'timestamp': datetime.now().isoformat(),
                'latitude': round(random.uniform(35.4, 35.8), 6),
                'longitude': round(random.uniform(139.5, 140.2), 6),
                'speed_knots': round(random.uniform(5, 20), 1),
                'heading': round(random.uniform(0, 360), 1),
                'emergency_status': 'Normal' if random.random() > 0.7 else 'Emergency',
                'anomaly_score': round(random.uniform(0, 1), 2),
                'confidence_score': round(random.uniform(85, 95), 1)
            })
        return data
    
    def generate_spill_data(self):
        """Generate realistic oil spill detection data"""
        data = []
        for i in range(5):
            data.append({
                'location': f'Location-{i+1}',
                'timestamp': datetime.now().isoformat(),
                'spill_detected': random.random() > 0.8,
                'spill_type': 'Oil' if random.random() > 0.5 else 'Chemical',
                'severity_level': random.choice(['Low', 'Medium', 'High']),
                'affected_area_km2': round(random.uniform(0.1, 5.0), 2),
                'confidence_score': round(random.uniform(85, 95), 1)
            })
        return data
    
    def get_highest_flood_risk(self) -> str:
        """Get highest current flood risk level"""
        flood_data = self.current_data.get('flood_data', [])
        if not flood_data:
            return 'Low'
        
        # Convert to list of risk percentages
        risk_values = [item.get('risk_percentage', 0) for item in flood_data]
        if not risk_values:
            return 'Low'
            
        highest_risk = max(risk_values)
        if highest_risk >= 70:
            return 'High'
        elif highest_risk >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current system status for dashboard"""
        return {
            'system_status': 'Active',
            'last_update': self.current_data.get('timestamp'),
            'active_alerts': len([a for a in self.current_data.get('alerts', []) if a.get('status') == 'active']),
            'flood_risk_level': self.get_highest_flood_risk(),
            'ship_emergencies': len([s for s in self.current_data.get('ship_data', []) if s.get('emergency_status') == 'Emergency']),
            'active_spills': len([s for s in self.current_data.get('spill_data', []) if s.get('spill_detected')]),
        }
    
    def export_data_for_powerbi(self):
        """Export current data to CSV files for Power BI"""
        output_dir = "./data/outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Export flood predictions
        if self.current_data['flood_data']:
            flood_df = pd.DataFrame(self.current_data['flood_data'])
            flood_df.to_csv(f"{output_dir}/flood_predictions.csv", index=False)
        
        # Export ship emergencies
        if self.current_data['ship_data']:
            ship_df = pd.DataFrame(self.current_data['ship_data'])
            ship_df.to_csv(f"{output_dir}/ship_emergencies.csv", index=False)
        
        # Export spill detections
        if self.current_data['spill_data']:
            spill_df = pd.DataFrame(self.current_data['spill_data'])
            spill_df.to_csv(f"{output_dir}/spill_detections.csv", index=False)
        
        # Export alerts
        if self.current_data['alerts']:
            alerts_df = pd.DataFrame(self.current_data['alerts'])
            alerts_df.to_csv(f"{output_dir}/alerts.csv", index=False)
        
        # Export digital twin state
        if 'digital_twin' in self.current_data:
            twin_df = pd.DataFrame([self.current_data['digital_twin']])
            twin_df.to_csv(f"{output_dir}/digital_twin.csv", index=False)
        
        logger.info(f"Data exported to {output_dir} for Power BI")
    
    async def run_simulation_cycle(self):
        """Run one complete simulation cycle"""
        try:
            # 1. Generate simulated data
            logger.info("Generating simulated data...")
            flood_data = self.generate_flood_data()
            ship_data = self.generate_ship_data()
            spill_data = self.generate_spill_data()
            
            # 2. Store current data
            self.current_data = {
                'flood_data': flood_data,
                'ship_data': ship_data,
                'spill_data': spill_data,
                'alerts': [],
                'digital_twin': {
                    'timestamp': datetime.now().isoformat(),
                    'system_status': 'Active',
                    'data_sources': '5 active',
                    'uptime': '24/7'
                }
            }
            
            # 3. Check for alerts
            logger.info("Checking for alerts...")
            new_alerts = []
            
            # Simple alert logic
            if flood_data and any(item['risk_percentage'] > 70 for item in flood_data):
                new_alerts.append({
                    'alert_type': 'Flood Risk',
                    'level': 'High',
                    'title': 'High Flood Risk Detected',
                    'message': 'Flood risk exceeded 70% threshold.',
                    'location': 'Multiple locations',
                    'reason': 'Risk threshold exceeded',
                    'status': 'active',
                    'timestamp': datetime.now().isoformat()
                })
            
            if ship_data and any(item['emergency_status'] == 'Emergency' for item in ship_data):
                new_alerts.append({
                    'alert_type': 'Ship Emergency',
                    'level': 'Medium',
                    'title': 'Ship Emergency Detected',
                    'message': 'Ship emergency detected.',
                    'location': 'Maritime routes',
                    'reason': 'Emergency status detected',
                    'status': 'active',
                    'timestamp': datetime.now().isoformat()
                })
            
            if spill_data and any(item['spill_detected'] for item in spill_data):
                new_alerts.append({
                    'alert_type': 'Oil Spill',
                    'level': 'High',
                    'title': 'Oil Spill Detected',
                    'message': 'Oil spill detected.',
                    'location': 'Coastal waters',
                    'reason': 'Spill detected',
                    'status': 'active',
                    'timestamp': datetime.now().isoformat()
                })
            
            self.current_data['alerts'] = new_alerts
            
            # 4. Export data for Power BI
            self.export_data_for_powerbi()
            
            logger.info(f"Simulation cycle completed. Generated {len(new_alerts)} alerts")
            
        except Exception as e:
            logger.error(f"Error in simulation cycle: {str(e)}")
    
    async def main():
        """Main function to run AquaGuard AI system"""
        aquaguard = AquaGuardAI()
        
        logger.info("Starting AquaGuard AI Simulation...")
        logger.info("Press Ctrl+C to stop simulation")
        
        try:
            while True:
                await aquaguard.run_simulation_cycle()
                # Wait for next cycle (configurable interval)
                await asyncio.sleep(60)  # Run every minute for demo
            
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
