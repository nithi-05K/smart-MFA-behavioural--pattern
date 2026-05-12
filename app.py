from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from twilio.rest import Client
import random

app = Flask(__name__)
CORS(app)

# Load model
model = pickle.load(open("behavior_model.pkl", "rb"))

# ---------------- TWILIO SETUP ----------------
account_sid = "YOUR_SID"
auth_token = "YOUR_TOKEN"
twilio_number = "+12603466726"

client = Client(account_sid, auth_token)

otp_store = {}

# ---------------- ML PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = [
        data["cpm"],
        data["dwell_avg"],
        data["flight_avg"],
        data["pressure_touch"],
        data["scroll_x"],
        data["scroll_y"],
        data["tilt_angle"]
    ]

    final = np.array(features).reshape(1, -1)
    prediction = model.predict(final)

    return jsonify({"result": int(prediction[0])})

# ---------------- SEND OTP ----------------
@app.route("/send_otp", methods=["POST"])
def send_otp():
    phone = request.json["phone"]

    otp = str(random.randint(1000, 9999))
    otp_store[phone] = otp

    client.messages.create(
        body=f"Your OTP is {otp}",
        from_=twilio_number,
        to=phone
    )

    return jsonify({"message": "OTP sent"})

# ---------------- VERIFY OTP ----------------
@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    phone = request.json["phone"]
    otp = request.json["otp"]

    if otp_store.get(phone) == otp:
        return jsonify({"status": "verified"})
    else:
        return jsonify({"status": "failed"})

if __name__ == "__main__":
    app.run(debug=True)