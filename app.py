from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Global storage
sensor_data = {
    "gsr": 0,
    "temp": 0,
    "hr": 0,
    "stress": "No Stress"
}

# --- Stress Logic ---
def determine_stress(bpm, gsr, temp):
    score = 0
    
    if gsr == 4: score += 4
    elif gsr == 3: score += 2
    elif gsr == 2: score += 1
    
    if bpm > 120: score += 3
    elif bpm > 90: score += 1
    
    if temp < 35.0 or temp > 38.0: score += 1

    if score >= 7: return "Extreme"
    if score >= 5: return "High"
    if score >= 3: return "Medium"
    if score >= 2: return "Low"
    return "No Stress"

# Homepage
@app.route('/')
def home():
    return render_template('index.html', data=sensor_data)

# ESP32 update route
@app.route('/update/gsr/<int:gsr>/temp/<float:temp>/hr/<int:hr>')
def update(gsr, temp, hr):
    sensor_data["gsr"] = gsr
    sensor_data["temp"] = temp
    sensor_data["hr"] = hr

    # Calculate stress
    sensor_data["stress"] = determine_stress(hr, gsr, temp)

    return "Data received successfully!"

# 🔥 NEW: API for live updates
@app.route('/data')
def get_data():
    return jsonify(sensor_data)

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)