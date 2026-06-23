from flask import Flask, jsonify, render_template, request
import pickle
import numpy as np
import random

app = Flask(__name__)
otp_store = {}

# Load trained model
with open("behavior_model.pkl", "rb") as f:
    model = pickle.load(f)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Prediction
@app.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE HIT")

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body is required"}), 400

        cpm = float(data["cpm"])
        dwell_avg = float(data["dwell_avg"])
        flight_avg = float(data["flight_avg"])
        pressure_touch = float(data["pressure_touch"])
        scroll_x = float(data["scroll_x"])
        scroll_y = float(data["scroll_y"])
        tilt_angle = float(data["tilt_angle"])

        features = np.array([[
            cpm,
            dwell_avg,
            flight_avg,
            pressure_touch,
            scroll_x,
            scroll_y,
            tilt_angle
        ]])

        prediction = model.predict(features)[0]
        if hasattr(prediction, "item"):
            prediction = prediction.item()

        return jsonify({
            "result": prediction
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/send_otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    if not data or not data.get("phone"):
        return jsonify({"error": "Phone number is required"}), 400

    phone = data["phone"]
    otp = str(random.randint(1000, 9999))
    otp_store[phone] = otp
    print(f"OTP for {phone}: {otp}")

    return jsonify({"status": "sent"})


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    if not data or not data.get("phone") or not data.get("otp"):
        return jsonify({"error": "Phone number and OTP are required"}), 400

    phone = data["phone"]
    otp = data["otp"]

    if otp_store.get(phone) == otp:
        otp_store.pop(phone, None)
        return jsonify({"status": "verified"})

    return jsonify({"status": "invalid"}), 401

if __name__ == "__main__":
    app.run(debug=True)
