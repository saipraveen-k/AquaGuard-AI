# 🌊 AquaGuard AI - Project Structure

## 📁 Directory Structure

```
AquaGuard-AI/
├── 📄 README.md                    # Comprehensive project documentation
├── 📄 RESPONSIBLE_AI.md           # Microsoft AI Principles compliance
├── 📄 POWER_BI_DESIGN_GUIDE.md    # Complete Power BI blueprint
├── 📄 WEB_FRONTEND.md             # Web dashboard documentation
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env.example               # Environment configuration template
├── 📄 main.py                    # Main orchestrator and entry point
├── 📄 web_app.py                 # Flask web application (NEW!)
├── 📄 generate_sample_data.py    # Sample data generator for demos
├── 📄 deploy_azure.sh            # Azure deployment script (NEW!)
├── 📄 Procfile                   # Azure App Service config (NEW!)
│
├── 📁 modules/                   # Core AI and processing modules
│   ├── 📄 __init__.py
│   ├── 📄 flood_prediction.py     # Azure ML flood risk prediction
│   ├── 📄 ship_emergency.py      # AIS-based emergency detection
│   ├── 📄 oil_spill_detection.py # Azure AI Vision spill detection
│   ├── 📄 digital_twin.py        # Azure Maps simulation
│   ├── 📄 alert_system.py        # Alert management and notification
│   └── 📄 data_generator.py      # Real-time data simulation
│
├── 📁 models/                    # Trained ML models (auto-generated)
│   ├── 📄 flood_model.pkl
│   ├── 📄 flood_scaler.pkl
│   ├── 📄 ship_emergency_model.pkl
│   ├── 📄 ship_emergency_scaler.pkl
│   ├── 📄 spill_classifier.pkl
│   └── 📄 spill_scaler.pkl
│
├── 📁 data/                      # Data storage and outputs
│   ├── 📁 outputs/               # Generated CSV files for dashboards
│   │   ├── 📄 flood_predictions.csv
│   │   ├── 📄 ship_emergencies.csv
│   │   ├── 📄 spill_detections.csv
│   │   ├── 📄 alerts.csv
│   │   ├── 📄 digital_twin.csv
│   │   └── 📄 data_schemas.json
│   ├── 📁 images/                # Sample images for spill detection
│   └── 📁 raw/                   # Raw sensor data (production)
│
├── 📁 templates/                 # Web dashboard templates (NEW!)
│   └── 📄 dashboard.html         # Main web interface
│
├── 📁 docs/                      # Additional documentation
│   ├── 📄 api_documentation.md
│   ├── 📄 deployment_guide.md
│   └── 📄 technical_specifications.md
│
├── 📁 tests/                     # Unit and integration tests
│   ├── 📄 test_flood_prediction.py
│   ├── 📄 test_ship_emergency.py
│   ├── 📄 test_spill_detection.py
│   └── 📄 test_integration.py
│
└── 📁 scripts/                   # Utility and deployment scripts
    ├── 📄 setup_azure.py
    ├── 📄 deploy_models.py
    └── 📄 health_check.py
```

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Generate Sample Data**
```bash
python generate_sample_data.py
```

### 3. **Run AI Backend**
```bash
python main.py
```

### 4. **Launch Web Dashboard** (NEW!)
```bash
python web_app.py
# Open: http://localhost:5000
```

### 5. **Connect Power BI** (Optional)
- Open Power BI Desktop
- Connect to CSV files in `./data/outputs/`
- Follow `POWER_BI_DESIGN_GUIDE.md`

## 📊 Dual Interface Architecture

### 🌐 Web Dashboard (Real-Time Operations)
- **File**: `web_app.py` + `templates/dashboard.html`
- **Technology**: Flask + Microsoft Fluent UI
- **Features**: Real-time monitoring, mobile responsive
- **Access**: http://localhost:5000

### 📊 Power BI Dashboard (Strategic Analytics)
- **File**: `POWER_BI_DESIGN_GUIDE.md`
- **Technology**: Power BI Desktop
- **Features**: Deep analytics, historical trends
- **Access**: Power BI application

## 🎯 Key Components

### 🧠 AI Modules (6 Complete Implementations)
- **flood_prediction.py**: Azure ML with Random Forest
- **ship_emergency.py**: Anomaly detection with Isolation Forest
- **oil_spill_detection.py**: Azure AI Vision + Image Classification
- **digital_twin.py**: Azure Maps simulation and prediction
- **alert_system.py**: Intelligent alert management
- **data_generator.py**: Real-time data simulation

### 📱 Output Files
- **flood_predictions.csv**: Real-time flood risk analysis
- **ship_emergencies.csv**: Vessel emergency detection results
- **spill_detections.csv**: Oil/chemical spill monitoring
- **alerts.csv**: System alerts and notifications
- **digital_twin.csv**: Simulation predictions

## 🏆 Imagine Cup Ready

This complete MVP includes:
- ✅ Full working implementation
- ✅ Dual interface strategy (Web + Power BI)
- ✅ Microsoft Azure integration
- ✅ Real-time dashboard capabilities
- ✅ Mobile responsive design
- ✅ Comprehensive documentation
- ✅ Demo scenarios included

## 📞 Support
See `README.md` for detailed setup instructions and demo guide.
