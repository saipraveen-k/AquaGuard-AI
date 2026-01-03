"""
AquaGuard AI - Unified Flood, Ocean & Maritime Emergency Intelligence System
Main Orchestrator for Imagine Cup MVP

This module coordinates all AI modules and manages data flow for the demo.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import asyncio
import pandas as pd

# Import our custom modules
from modules.flood_prediction import FloodPredictor
from modules.ship_emergency import ShipEmergencyDetector
from modules.oil_spill_detection import OilSpillDetector
from modules.digital_twin import DigitalTwinSimulator
from modules.alert_system import AlertManager
from modules.data_generator import DataSimulator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AquaGuardAI:
    """Main orchestrator for AquaGuard AI system"""
    
    def __init__(self):
        self.flood_predictor = FloodPredictor()
        self.ship_detector = ShipEmergencyDetector()
        self.spill_detector = OilSpillDetector()
        self.digital_twin = DigitalTwinSimulator()
        self.alert_manager = AlertManager()
        self.data_simulator = DataSimulator()
        
        # Initialize data storage
        self.current_data = {
            'flood_data': [],
            'ship_data': [],
            'spill_data': [],
            'alerts': []
        }
        
        logger.info("AquaGuard AI System Initialized")
    
    async def run_simulation_cycle(self):
        """Run one complete simulation cycle"""
        try:
            # 1. Generate simulated data
            logger.info("Generating simulated data...")
            flood_data = self.data_simulator.generate_flood_data()
            ship_data = self.data_simulator.generate_ship_data()
            spill_images = self.data_simulator.generate_spill_scenarios()
            
            # 2. Process data through AI modules
            logger.info("Processing data through AI modules...")
            
            # Flood Prediction
            flood_predictions = []
            for data_point in flood_data:
                prediction = self.flood_predictor.predict_flood_risk(data_point)
                flood_predictions.append(prediction)
            
            # Ship Emergency Detection
            ship_emergencies = []
            for ship in ship_data:
                emergency = self.ship_detector.detect_emergency(ship)
                ship_emergencies.append(emergency)
            
            # Oil Spill Detection
            spill_detections = []
            for image_path, metadata in spill_images:
                detection = self.spill_detector.detect_spill(image_path, metadata)
                spill_detections.append(detection)
            
            # 3. Update Digital Twin
            logger.info("Updating Digital Twin simulation...")
            twin_state = self.digital_twin.update_state(
                flood_predictions, ship_emergencies, spill_detections
            )
            
            # 4. Check for alerts
            logger.info("Checking for alerts...")
            new_alerts = self.alert_manager.check_alerts(
                flood_predictions, ship_emergencies, spill_detections
            )
            
            # 5. Store current data
            self.current_data = {
                'flood_data': flood_predictions,
                'ship_data': ship_emergencies,
                'spill_data': spill_detections,
                'alerts': new_alerts,
                'digital_twin': twin_state,
                'timestamp': datetime.now().isoformat()
            }
            
            # 6. Export data for Power BI
            self.export_data_for_powerbi()
            
            logger.info(f"Simulation cycle completed. Generated {len(new_alerts)} alerts")
            
        except Exception as e:
            logger.error(f"Error in simulation cycle: {str(e)}")
    
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
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current system status for dashboard"""
        return {
            'system_status': 'Active',
            'last_update': self.current_data.get('timestamp'),
            'active_alerts': len([a for a in self.current_data.get('alerts', []) if a['status'] == 'active']),
            'flood_risk_level': self.get_highest_flood_risk(),
            'ship_emergencies': len([s for s in self.current_data.get('ship_data', []) if s['emergency_status'] == 'Emergency']),
            'active_spills': len([s for s in self.current_data.get('spill_data', []) if s['spill_detected']]),
        }
    
    def get_highest_flood_risk(self) -> str:
        """Get highest current flood risk level"""
        flood_data = self.current_data.get('flood_data', [])
        if not flood_data:
            return 'Low'
        
        highest_risk = max([f['risk_percentage'] for f in flood_data])
        if highest_risk >= 70:
            return 'High'
        elif highest_risk >= 40:
            return 'Medium'
        else:
            return 'Low'

async def main():
    """Main function to run the AquaGuard AI system"""
    aquaguard = AquaGuardAI()
    
    logger.info("Starting AquaGuard AI Simulation...")
    logger.info("Press Ctrl+C to stop the simulation")
    
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
