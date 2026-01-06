return 'Low'

async def run_simulation_loop():
=======
        else:
            return 'Low'

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the main dashboard"""
    with open("templates/dashboard.html", "r") as f:
        return f.read()

@app.get("/api/status")
async def get_system_status():
    """Get current system status"""
    if not aquaguard_instance:
        raise HTTPException(status_code=503, detail="System not initialized")
    return aquaguard_instance.get_current_status()

@app.get("/api/data/{data_type}")
async def get_data(data_type: str):
    """Get specific data type (flood_data, ship_data, spill_data, alerts)"""
    if not aquaguard_instance:
        raise HTTPException(status_code=503, detail="System not initialized")

    if data_type not in aquaguard_instance.current_data:
        raise HTTPException(status_code=404, detail="Data type not found")

    return JSONResponse(content=aquaguard_instance.current_data[data_type])

@app.post("/api/trigger-simulation")
async def trigger_simulation():
    """Manually trigger a simulation cycle"""
    if not aquaguard_instance:
        raise HTTPException(status_code=503, detail="System not initialized")

    try:
        await aquaguard_instance.run_simulation_cycle()
        return {"status": "success", "message": "Simulation cycle completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

async def run_simulation_loop():
