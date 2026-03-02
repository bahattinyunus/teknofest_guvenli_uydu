import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Global store for the latest telemetry of all satellites
swarm_telemetry = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/telemetry', methods=['GET', 'POST'])
def telemetry():
    global swarm_telemetry
    if request.method == 'POST':
        data = request.json
        sat_id = data.get("satellite_id", "UNKNOWN")
        swarm_telemetry[sat_id] = data
        return jsonify({"status": "received", "sat_id": sat_id}), 200
    else:
        # Return all telemetry for the map/list
        return jsonify(swarm_telemetry)

@app.route('/api/telemetry/<sat_id>', methods=['GET'])
def telemetry_single(sat_id):
    return jsonify(swarm_telemetry.get(sat_id, {}))

@app.route('/api/command', methods=['POST'])
def send_command():
    cmd = request.json.get('command')
    print(f"[GS] QUEUING COMMAND: {cmd}")
    # In a real system, this would be queued for the next uplink window.
    return jsonify({"status": "queued", "command": cmd}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
