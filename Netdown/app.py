from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model & scaler
model = joblib.load("network_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    severity = None

    if request.method == "POST":
        # Get form data
        flow_duration = float(request.form["flow_duration"])
        flow_bytes = float(request.form["flow_bytes"])
        flow_packets = float(request.form["flow_packets"])
        packet_length = float(request.form["packet_length"])

        # Backend safety validation (clamping)
        flow_duration = min(max(flow_duration, 1), 5000)
        flow_bytes = min(max(flow_bytes, 1000), 2_000_000)
        flow_packets = min(max(flow_packets, 1000), 2_000_000)
        packet_length = min(max(packet_length, 0.1), 10)

        # Prepare dataframe
        data = pd.DataFrame([[
            flow_duration,
            flow_bytes,
            flow_packets,
            packet_length
        ]], columns=[
            "Flow Duration",
            "Flow Bytes/s",
            "Flow Packets/s",
            "Packet Length Mean"
        ])

        # Predict
        scaled_data = scaler.transform(data)
        seconds = max(0, model.predict(scaled_data)[0])

        # Human-friendly time display
        if seconds < 60:
            prediction = f"🚨 Network failure predicted in {int(seconds)} seconds"
        else:
            minutes = seconds / 60
            prediction = f"🚨 Network failure predicted in {minutes:.2f} minutes"

        # Severity logic
        if seconds < 120:
            severity = "Critical 🔴"
        elif seconds < 300:
            severity = "Warning 🟡"
        else:
            severity = "Stable 🟢"

    return render_template("index.html",
                           prediction=prediction,
                           severity=severity)

if __name__ == "__main__":
    app.run(debug=True)
