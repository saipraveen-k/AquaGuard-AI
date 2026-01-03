"""
Alert System Module for AquaGuard AI
Manages alert generation, prioritization, and notification
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class AlertType(Enum):
    FLOOD = "Flood"
    SHIP_EMERGENCY = "Ship Emergency"
    OIL_SPILL = "Oil Spill"
    SYSTEM = "System"

class AlertManager:
    """Manages alert generation and distribution for AquaGuard AI"""
    
    def __init__(self):
        self.alerts = []
        self.alert_thresholds = {
            'flood_risk': 70,  # percentage
            'ship_anomaly': 0.8,  # anomaly score
            'spill_confidence': 0.7  # confidence score
        }
        
        # Alert history for deduplication
        self.recent_alerts = {}
        self.alert_cooldown_minutes = 15
        
        logger.info("Alert Manager initialized")
    
    def check_alerts(self, flood_predictions: List[Dict], 
                    ship_emergencies: List[Dict], 
                    spill_detections: List[Dict]) -> List[Dict]:
        """Check all data sources and generate alerts"""
        
        new_alerts = []
        
        # Check flood predictions
        flood_alerts = self._check_flood_alerts(flood_predictions)
        new_alerts.extend(flood_alerts)
        
        # Check ship emergencies
        ship_alerts = self._check_ship_alerts(ship_emergencies)
        new_alerts.extend(ship_alerts)
        
        # Check spill detections
        spill_alerts = self._check_spill_alerts(spill_detections)
        new_alerts.extend(spill_alerts)
        
        # Update alert history
        self._update_alert_history(new_alerts)
        
        # Store alerts
        self.alerts.extend(new_alerts)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        logger.info(f"Generated {len(new_alerts)} new alerts")
        return new_alerts
    
    def _check_flood_alerts(self, flood_predictions: List[Dict]) -> List[Dict]:
        """Check flood predictions for alert conditions"""
        alerts = []
        
        for prediction in flood_predictions:
            risk_percentage = prediction['risk_percentage']
            risk_level = prediction['risk_level']
            
            # Determine alert level
            if risk_percentage >= 90:
                alert_level = AlertLevel.CRITICAL
            elif risk_percentage >= 70:
                alert_level = AlertLevel.HIGH
            elif risk_percentage >= 50:
                alert_level = AlertLevel.MEDIUM
            else:
                alert_level = AlertLevel.LOW
            
            # Generate alert if above threshold
            if risk_percentage >= self.alert_thresholds['flood_risk']:
                alert = self._create_alert(
                    alert_type=AlertType.FLOOD,
                    level=alert_level,
                    title=f"Flood Risk Alert - {prediction['location_name']}",
                    message=self._generate_flood_alert_message(prediction),
                    source_data=prediction,
                    location={
                        'latitude': prediction['latitude'],
                        'longitude': prediction['longitude'],
                        'name': prediction['location_name']
                    }
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_ship_alerts(self, ship_emergencies: List[Dict]) -> List[Dict]:
        """Check ship data for emergency alerts"""
        alerts = []
        
        for ship in ship_emergencies:
            if ship['emergency_status'] == 'Emergency':
                # Determine alert level based on anomaly score
                anomaly_score = ship['anomaly_score']
                
                if anomaly_score <= -0.8:
                    alert_level = AlertLevel.CRITICAL
                elif anomaly_score <= -0.5:
                    alert_level = AlertLevel.HIGH
                else:
                    alert_level = AlertLevel.MEDIUM
                
                alert = self._create_alert(
                    alert_type=AlertType.SHIP_EMERGENCY,
                    level=alert_level,
                    title=f"Ship Emergency - {ship['ship_name']}",
                    message=self._generate_ship_alert_message(ship),
                    source_data=ship,
                    location={
                        'latitude': ship['latitude'],
                        'longitude': ship['longitude'],
                        'name': f"Vessel {ship['ship_name']} ({ship['ship_type']})"
                    }
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_spill_alerts(self, spill_detections: List[Dict]) -> List[Dict]:
        """Check spill detections for alert conditions"""
        alerts = []
        
        for detection in spill_detections:
            if detection['spill_detected']:
                confidence = detection['confidence_score']
                severity = detection['severity_level']
                
                # Determine alert level
                if severity == 'High' and confidence >= 0.8:
                    alert_level = AlertLevel.CRITICAL
                elif severity == 'High' or (severity == 'Medium' and confidence >= 0.7):
                    alert_level = AlertLevel.HIGH
                elif severity == 'Medium' or (severity == 'Low' and confidence >= 0.8):
                    alert_level = AlertLevel.MEDIUM
                else:
                    alert_level = AlertLevel.LOW
                
                # Only alert if confidence is above threshold
                if confidence >= self.alert_thresholds['spill_confidence']:
                    alert = self._create_alert(
                        alert_type=AlertType.OIL_SPILL,
                        level=alert_level,
                        title=f"{detection['spill_type']} Spill Detected - {detection['location_name']}",
                        message=self._generate_spill_alert_message(detection),
                        source_data=detection,
                        location={
                            'latitude': detection['latitude'],
                            'longitude': detection['longitude'],
                            'name': detection['location_name']
                        }
                    )
                    alerts.append(alert)
        
        return alerts
    
    def _create_alert(self, alert_type: AlertType, level: AlertLevel, 
                     title: str, message: str, source_data: Dict, 
                     location: Dict) -> Dict:
        """Create a new alert"""
        
        alert_id = str(uuid.uuid4())
        
        alert = {
            'alert_id': alert_id,
            'timestamp': datetime.now().isoformat(),
            'alert_type': alert_type.value,
            'level': level.value,
            'title': title,
            'message': message,
            'status': 'active',
            'location': location,
            'source_data': source_data,
            'actions_required': self._get_required_actions(alert_type, level),
            'estimated_impact': self._estimate_impact(alert_type, level, source_data),
            'coordination_needs': self._get_coordination_needs(alert_type),
            'power_bi_visual_config': self._get_power_bi_config(alert_type, level)
        }
        
        return alert
    
    def _generate_flood_alert_message(self, prediction: Dict) -> str:
        """Generate flood alert message"""
        risk_level = prediction['risk_level']
        time_to_flood = prediction['time_to_flood_hours']
        
        if risk_level == 'High' and time_to_flood <= 6:
            return f"CRITICAL: Flood risk {prediction['risk_percentage']}%. Expected flooding in {time_to_flood:.1f} hours. Immediate action required."
        elif risk_level == 'Medium':
            return f"WARNING: Flood risk {prediction['risk_percentage']}%. Monitor conditions and prepare for potential flooding in {time_to_flood:.1f} hours."
        else:
            return f"ADVISORY: Elevated flood risk {prediction['risk_percentage']}%. Continue monitoring."
    
    def _generate_ship_alert_message(self, ship: Dict) -> str:
        """Generate ship emergency alert message"""
        anomaly_type = ship['anomaly_type']
        ship_name = ship['ship_name']
        
        return f"EMERGENCY: {ship_name} showing {anomaly_type.replace('_', ' ').title()}. Last known position: {ship['latitude']:.4f}, {ship['longitude']:.4f}. Immediate response required."
    
    def _generate_spill_alert_message(self, detection: Dict) -> str:
        """Generate spill alert message"""
        spill_type = detection['spill_type']
        severity = detection['severity_level']
        area = detection['affected_area_km2']
        
        return f"ALERT: {severity} {spill_type} spill detected. Affected area: {area:.3f} km². Confidence: {detection['confidence_score']:.1%}. Deploy containment team."
    
    def _get_required_actions(self, alert_type: AlertType, level: AlertLevel) -> List[str]:
        """Get required actions based on alert type and level"""
        actions = []
        
        if alert_type == AlertType.FLOOD:
            if level in [AlertLevel.HIGH, AlertLevel.CRITICAL]:
                actions.extend([
                    "Issue evacuation orders if necessary",
                    "Deploy flood barriers",
                    "Monitor water levels continuously",
                    "Coordinate with emergency services"
                ])
            else:
                actions.extend([
                    "Monitor weather conditions",
                    "Prepare emergency equipment",
                    "Notify local authorities"
                ])
        
        elif alert_type == AlertType.SHIP_EMERGENCY:
            actions.extend([
                "Contact vessel via emergency channels",
                "Deploy rescue vessels if needed",
                "Coordinate with Coast Guard",
                "Monitor nearby vessel traffic"
            ])
        
        elif alert_type == AlertType.OIL_SPILL:
            if level in [AlertLevel.HIGH, AlertLevel.CRITICAL]:
                actions.extend([
                    "Deploy containment booms immediately",
                    "Activate spill response team",
                    "Notify environmental agencies",
                    "Monitor spread trajectory"
                ])
            else:
                actions.extend([
                    "Assess spill size and type",
                    "Prepare containment equipment",
                    "Monitor environmental impact"
                ])
        
        return actions
    
    def _estimate_impact(self, alert_type: AlertType, level: AlertLevel, 
                       source_data: Dict) -> Dict[str, Any]:
        """Estimate potential impact of the alert"""
        
        impact = {
            'human_safety': 'Unknown',
            'environmental': 'Unknown',
            'economic': 'Unknown',
            'infrastructure': 'Unknown'
        }
        
        if alert_type == AlertType.FLOOD:
            risk_percentage = source_data.get('risk_percentage', 0)
            if risk_percentage >= 80:
                impact.update({
                    'human_safety': 'High Risk',
                    'environmental': 'Moderate',
                    'economic': 'High',
                    'infrastructure': 'High Risk'
                })
            elif risk_percentage >= 60:
                impact.update({
                    'human_safety': 'Moderate Risk',
                    'environmental': 'Low',
                    'economic': 'Moderate',
                    'infrastructure': 'Moderate Risk'
                })
        
        elif alert_type == AlertType.SHIP_EMERGENCY:
            impact.update({
                'human_safety': 'High Risk',
                'environmental': 'Low',
                'economic': 'Moderate',
                'infrastructure': 'Low'
            })
        
        elif alert_type == AlertType.OIL_SPILL:
            area = source_data.get('affected_area_km2', 0)
            if area > 1.0:
                impact.update({
                    'human_safety': 'Low',
                    'environmental': 'High Risk',
                    'economic': 'High',
                    'infrastructure': 'Low'
                })
            else:
                impact.update({
                    'human_safety': 'Low',
                    'environmental': 'Moderate',
                    'economic': 'Moderate',
                    'infrastructure': 'Low'
                })
        
        return impact
    
    def _get_coordination_needs(self, alert_type: AlertType) -> List[str]:
        """Get coordination requirements for alert type"""
        coordination_map = {
            AlertType.FLOOD: [
                "Local Emergency Management",
                "Weather Service",
                "Transportation Authorities",
                "Health Services"
            ],
            AlertType.SHIP_EMERGENCY: [
                "Coast Guard",
                "Port Authority",
                "Maritime Rescue Coordination Center",
                "Shipping Company"
            ],
            AlertType.OIL_SPILL: [
                "Environmental Protection Agency",
                "Coast Guard",
                "Local Wildlife Agencies",
                "Cleanup Contractors"
            ]
        }
        
        return coordination_map.get(alert_type, ["Local Authorities"])
    
    def _get_power_bi_config(self, alert_type: AlertType, level: AlertLevel) -> Dict:
        """Get Power BI visualization configuration for alert"""
        
        color_map = {
            AlertLevel.LOW: "#28a745",      # Green
            AlertLevel.MEDIUM: "#ffc107",   # Yellow
            AlertLevel.HIGH: "#fd7e14",     # Orange
            AlertLevel.CRITICAL: "#dc3545"  # Red
        }
        
        icon_map = {
            AlertType.FLOOD: "🌊",
            AlertType.SHIP_EMERGENCY: "🚢",
            AlertType.OIL_SPILL: "🛢️"
        }
        
        return {
            'color': color_map[level],
            'icon': icon_map[alert_type],
            'priority_order': {
                AlertLevel.CRITICAL: 1,
                AlertLevel.HIGH: 2,
                AlertLevel.MEDIUM: 3,
                AlertLevel.LOW: 4
            }[level],
            'auto_refresh': True,
            'notification_sound': level in [AlertLevel.HIGH, AlertLevel.CRITICAL]
        }
    
    def _update_alert_history(self, new_alerts: List[Dict]):
        """Update alert history for deduplication"""
        current_time = datetime.now()
        
        for alert in new_alerts:
            alert_key = f"{alert['alert_type']}_{alert['location']['name']}"
            
            # Check if similar alert was recently generated
            if alert_key in self.recent_alerts:
                last_time = self.recent_alerts[alert_key]
                time_diff = (current_time - last_time).total_seconds() / 60
                
                if time_diff < self.alert_cooldown_minutes:
                    # Skip this alert to avoid duplication
                    continue
            
            # Update recent alerts
            self.recent_alerts[alert_key] = current_time
        
        # Clean old entries
        cutoff_time = current_time - timedelta(hours=1)
        self.recent_alerts = {
            k: v for k, v in self.recent_alerts.items() 
            if v > cutoff_time
        }
    
    def get_active_alerts(self) -> List[Dict]:
        """Get currently active alerts"""
        return [alert for alert in self.alerts if alert['status'] == 'active']
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of current alert status"""
        active_alerts = self.get_active_alerts()
        
        summary = {
            'total_active_alerts': len(active_alerts),
            'critical_alerts': len([a for a in active_alerts if a['level'] == 'Critical']),
            'high_alerts': len([a for a in active_alerts if a['level'] == 'High']),
            'medium_alerts': len([a for a in active_alerts if a['level'] == 'Medium']),
            'low_alerts': len([a for a in active_alerts if a['level'] == 'Low']),
            'alert_types': {
                'flood': len([a for a in active_alerts if a['alert_type'] == 'Flood']),
                'ship_emergency': len([a for a in active_alerts if a['alert_type'] == 'Ship Emergency']),
                'oil_spill': len([a for a in active_alerts if a['alert_type'] == 'Oil Spill'])
            },
            'last_update': datetime.now().isoformat()
        }
        
        return summary
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert['alert_id'] == alert_id:
                alert['status'] = 'acknowledged'
                alert['acknowledged_timestamp'] = datetime.now().isoformat()
                logger.info(f"Alert {alert_id} acknowledged")
                return True
        return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get alert system information for documentation"""
        return {
            'system_version': '1.0',
            'alert_types': [t.value for t in AlertType],
            'alert_levels': [l.value for l in AlertLevel],
            'thresholds': self.alert_thresholds,
            'cooldown_period_minutes': self.alert_cooldown_minutes,
            'max_history_size': 100,
            'power_bi_integration': True,
            'responsible_ai_compliance': True
        }
