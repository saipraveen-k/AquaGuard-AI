"""
Azure Web App Frontend for AquaGuard AI
Microsoft-preferred technology stack: Azure App Service + React + Azure Functions
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="../templates")
CORS(app)  # Enable CORS for Azure App Service

# Data paths
DATA_DIR = "./data/outputs"

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/flood-data')
def get_flood_data():
    """API endpoint for flood prediction data"""
    try:
        df = pd.read_csv(f"{DATA_DIR}/flood_predictions.csv")
        # Get recent flood predictions
        recent_floods = df.tail(10).to_dict('records')
        return jsonify({
            'success': True,
            'data': recent_floods,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error loading flood data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ship-data')
def get_ship_data():
    """API endpoint for ship emergency data"""
    try:
        df = pd.read_csv(f"{DATA_DIR}/ship_emergencies.csv")
        # Get recent ship data
        recent_ships = df.tail(20).to_dict('records')
        return jsonify({
            'success': True,
            'data': recent_ships,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error loading ship data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/spill-data')
def get_spill_data():
    """API endpoint for spill detection data"""
    try:
        df = pd.read_csv(f"{DATA_DIR}/spill_detections.csv")
        # Get recent spill detections
        recent_spills = df.tail(10).to_dict('records')
        return jsonify({
            'success': True,
            'data': recent_spills,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error loading spill data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/alerts')
def get_alerts():
    """API endpoint for system alerts"""
    try:
        df = pd.read_csv(f"{DATA_DIR}/alerts.csv")
        # Get active alerts
        active_alerts = df[df['status'] == 'active'].tail(10).to_dict('records')
        return jsonify({
            'success': True,
            'alerts': active_alerts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error loading alerts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/digital-twin')
def get_digital_twin():
    """API endpoint for digital twin simulation"""
    try:
        df = pd.read_csv(f"{DATA_DIR}/digital_twin.csv")
        latest_data = df.tail(1).to_dict('records')[0]
        return jsonify({
            'success': True,
            'data': latest_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error loading digital twin data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/kpi-summary')
def get_kpi_summary():
    """API endpoint for KPI summary"""
    try:
        # Load all data
        flood_df = pd.read_csv(f"{DATA_DIR}/flood_predictions.csv")
        ship_df = pd.read_csv(f"{DATA_DIR}/ship_emergencies.csv")
        spill_df = pd.read_csv(f"{DATA_DIR}/spill_detections.csv")
        alerts_df = pd.read_csv(f"{DATA_DIR}/alerts.csv")
        
        # Calculate KPIs
        kpis = {
            'flood_risk': {
                'current': float(flood_df['risk_percentage'].iloc[-1]) if not flood_df.empty else 0,
                'level': flood_df['risk_level'].iloc[-1] if not flood_df.empty else 'Low',
                'trend': 'increasing' if len(flood_df) > 1 and flood_df['risk_percentage'].iloc[-1] > flood_df['risk_percentage'].iloc[-2] else 'stable'
            },
            'ship_emergencies': {
                'active': int(len(ship_df[ship_df['emergency_status'] == 'Emergency'])),
                'total_monitored': int(len(ship_df['mmsi'].unique())),
                'anomaly_rate': float(len(ship_df[ship_df['emergency_status'] == 'Emergency']) / len(ship_df) * 100) if not ship_df.empty else 0
            },
            'spill_detections': {
                'active': int(len(spill_df[spill_df['spill_detected'] == True])),
                'total_area': float(spill_df[spill_df['spill_detected'] == True]['affected_area_km2'].sum()) if not spill_df.empty else 0,
                'severity_breakdown': {
                    'Low': int(len(spill_df[(spill_df['spill_detected'] == True) & (spill_df['severity_level'] == 'Low')])),
                    'Medium': int(len(spill_df[(spill_df['spill_detected'] == True) & (spill_df['severity_level'] == 'Medium')])),
                    'High': int(len(spill_df[(spill_df['spill_detected'] == True) & (spill_df['severity_level'] == 'High')])),
                }
            },
            'alerts': {
                'active': int(len(alerts_df[alerts_df['status'] == 'active'])),
                'critical': int(len(alerts_df[(alerts_df['status'] == 'active') & (alerts_df['level'] == 'Critical')])),
                'high': int(len(alerts_df[(alerts_df['status'] == 'active') & (alerts_df['level'] == 'High')])),
                'total_today': int(len(alerts_df))
            }
        }
        
        return jsonify({
            'success': True,
            'kpis': kpis,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error calculating KPIs: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/health')
def health_check():
    """Health check endpoint for Azure App Service"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'service': 'AquaGuard AI Web Frontend'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
