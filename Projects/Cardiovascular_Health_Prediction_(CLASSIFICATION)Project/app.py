from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model/cardio_model.pkl", "rb"))

# Load optimal threshold
with open("model/threshold.txt") as f:
    THRESHOLD = float(f.read())

# Feature engineering helpers
def age_group(age):
    if age < 40:
        return 0
    elif age < 55:
        return 1
    else:
        return 2

def cholesterol_category(totChol):
    if totChol < 200:
        return 0
    elif totChol < 240:
        return 1
    else:
        return 2

def bmi_category(bmi):
    if bmi < 18.5:
        return 0
    elif bmi < 25:
        return 1
    elif bmi < 30:
        return 2
    else:
        return 3

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Raw features
    age = data["age"]
    sex = data["sex"]
    is_smoking = data["is_smoking"]
    cigsPerDay = data["cigsPerDay"]
    BPMeds = data["BPMeds"]
    prevalentHyp = data["prevalentHyp"]
    totChol = data["totChol"]
    sysBP = data["sysBP"]
    diaBP = data["diaBP"]
    heartRate = data["heartRate"]
    glucose = data["glucose"]
    height = data["height"]
    weight = data["weight"]

    # Derived features
    bmi = weight / ((height / 100) ** 2)
    pulse_pressure = sysBP - diaBP

    # Feature vector (same order as training)
    features = np.array([[
        age, sex, is_smoking, cigsPerDay, BPMeds, prevalentHyp,
        totChol, sysBP, diaBP, bmi, heartRate, glucose,
        age_group(age), cholesterol_category(totChol),
        bmi_category(bmi), pulse_pressure
    ]])

    # Prediction
    proba = model.predict_proba(features)[0][1]
    prediction = int(proba >= THRESHOLD)

    return jsonify({
        "risk": "High Risk" if prediction == 1 else "Low Risk",
        "probability": round(proba * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
