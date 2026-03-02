import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Global store for the latest telemetry
latest_telemetry = {
    "payload": "Waiting for data...",
    "signature": "N/A",
    "metadata": {},
    "decrypted": {}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/telemetry', methods=['GET', 'POST'])
def telemetry():
    global latest_telemetry
    if request.method == 'POST':
        data = request.json
        # In a real GS, we would decrypt here. 
        # For simplicity in this demo, the simulator might send the decrypted version or we mock it.
        latest_telemetry = data
        return jsonify({"status": "received"}), 200
    else:
        return jsonify(latest_telemetry)

@app.route('/api/command', methods=['POST'])
def send_command():
    cmd = request.json.get('command')
    print(f"[GS] QUEUING COMMAND: {cmd}")
    # In a real system, this would be queued for the next uplink window.
    return jsonify({"status": "queued", "command": cmd}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
