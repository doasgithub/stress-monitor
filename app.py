from flask import Flask, render_template, jsonify
import joblib

app = Flask(__name__)

# Load ML model
model = joblib.load("model.pkl")

sensor_data = {
    "gsr": 0,
    "temp": 0,
    "hr": 0,
    "stress": "No Stress",
    "ml_stress": "Unknown"
}

# Rule-based logic
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

# ML prediction
def predict_ml(gsr, hr, temp):
    return model.predict([[gsr, hr, temp]])[0]

@app.route('/')
def home():
    return render_template('index.html', data=sensor_data)

@app.route('/update/gsr/<int:gsr>/temp/<float:temp>/hr/<int:hr>')
def update(gsr, temp, hr):
    sensor_data["gsr"] = gsr
    sensor_data["temp"] = temp
    sensor_data["hr"] = hr

    sensor_data["stress"] = determine_stress(hr, gsr, temp)
    sensor_data["ml_stress"] = predict_ml(gsr, hr, temp)

    return "OK"

@app.route('/data')
def get_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)