import pandas as pd
import numpy as np
import joblib # This is for saving your model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

# 1. Load your 1000 rows
df = pd.read_csv('synthetic_cicids_1000.csv')

# 2. Setup Features (X) and Target (y)
X = df[['Flow Duration', 'Flow Bytes/s', 'Flow Packets/s', 'Packet Length Mean']]
y = df['Seconds_To_Failure']

# 3. Scaling (Squish numbers between 0 and 1)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 4. Split data (80% Study, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 5. Train the Smart Brain (Random Forest)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Save the model and the scaler
joblib.dump(model, 'network_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Success! Your AI 'Brain' is trained and saved as 'network_model.pkl'.")

# 7. Quick Test with correct formatting
fake_data = pd.DataFrame([[1500.0, 300000.0, 500000.0, 6.0]],
                         columns=['Flow Duration', 'Flow Bytes/s', 'Flow Packets/s', 'Packet Length Mean'])
prediction = model.predict(scaler.transform(fake_data))
print(f"Prediction: Network failure in {max(0, prediction[0]):.2f} seconds!")