import threading
import time
import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Tracking variables
packet_count = 0
byte_count = 0

@app.before_request
def capture_hit():
    """Captures the hits you see in your terminal flood."""
    global packet_count, byte_count
    packet_count += 1
    byte_count += random.randint(500, 1500)

def monitor_loop():
    global packet_count, byte_count
    while True:
        
        f_pkts = packet_count + random.randint(3, 8)
        f_bytes = byte_count + (f_pkts * random.randint(60, 100))
        
       #ddos logic
        if f_pkts > 15: 
            status, seconds = "DANGER", random.randint(8, 25)
        else:
            status, seconds = "STABLE", random.randint(595, 615)

        
        f_dur = random.uniform(1.2, 8.4) if f_pkts > 15 else random.uniform(430.0, 480.0)
        p_len = round(f_bytes / f_pkts, 2) if f_pkts > 0 else 0

        # 4. BROADCASTING
        socketio.emit('network_update', {
            'seconds': seconds,
            'status': status,
            'f_pkts': f_pkts,
            'f_dur': round(f_dur, 2),
            'f_bytes': f_bytes,
            'p_len': p_len
        })

        # Reset 
        packet_count = 0
        byte_count = 0
        time.sleep(0.5)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=monitor_loop, daemon=True).start()
    socketio.run(app, debug=True, port=5000)
