from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import json
import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATA_FILE = "telemetry_history.json"

def save_data(data):
    history = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                history = json.load(f)
        except:
            history = []
    
    # Add timestamp if not present
    if "timestamp" not in data:
        data["timestamp"] = datetime.datetime.now().isoformat()
    
    history.append(data)
    
    # Keep last 100 entries to prevent file from growing indefinitely
    if len(history) > 100:
        history = history[-100:]
        
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=4)

@app.route("/api/data", methods=["POST"])
def receive_data():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    # Print to console for visibility
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Received AQI: {data.get('aqi')} | PM2.5: {data.get('pm25')}")
    
    save_data(data)
    return jsonify({"message": "Success", "status": "stored"}), 200

@app.route("/api/history", methods=["GET"])
def get_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return jsonify(json.load(f)), 200
    return jsonify([]), 200

@app.route("/api/download", methods=["GET"])
def download_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No data available"}), 404
        
    try:
        with open(DATA_FILE, "r") as f:
            raw_history = json.load(f)
            
        # Format history to match requested schema
        formatted_history = []
        for entry in raw_history:
            if not isinstance(entry, dict):
                continue
                
            formatted_entry = {
                "device_id": entry.get("device_id") or entry.get("device") or "ZENAB-UNIT-01",
                "timestamp": entry.get("timestamp"),
                "aqi": entry.get("aqi"),
                "pm25": entry.get("pm25"),
                "temperature": entry.get("temperature"),
                "humidity": entry.get("humidity"),
                "oxygen": entry.get("oxygen"),
                "latitude": entry.get("latitude"),
                "longitude": entry.get("longitude"),
                "power": entry.get("power"),
                "status": entry.get("status")
            }
            formatted_history.append(formatted_entry)
            
        json_data = json.dumps(formatted_history, indent=4)
        return Response(
            json_data,
            mimetype="application/json",
            headers={
                "Content-Disposition": "attachment; filename=telemetry_data.json",
                "Cache-Control": "no-cache"
            }
        )
    except Exception as e:
        print(f"Download Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return send_file("dashboard.html")

if __name__ == "__main__":
    print("ZENAB Backend started at http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
