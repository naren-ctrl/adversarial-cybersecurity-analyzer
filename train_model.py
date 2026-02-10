# train_model.py - Save in main project folder
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

print("=" * 60)
print("🤖 TRAINING ML MODEL")
print("=" * 60)

# Load data
df = pd.read_csv("data/raw/sample_logs.csv")
print(f"✅ Loaded {len(df)} logs")

# Simple preprocessing
def ip_to_number(ip):
    try:
        parts = ip.split('.')
        return sum(int(part) * (256 ** (3-i)) for i, part in enumerate(parts))
    except:
        return 0

# Prepare features
df['src_ip_num'] = df['src_ip'].apply(ip_to_number)
df['dst_ip_num'] = df['dst_ip'].apply(ip_to_number)

# Encode labels
label_map = {'normal': 0, 'brute_force': 1, 'port_scan': 2, 'dos': 3}
df['label_num'] = df['label'].map(label_map)

# Select features
features = ['src_port', 'dst_port', 'duration', 'bytes_sent', 'bytes_received', 'src_ip_num', 'dst_ip_num']
X = df[features]
y = df['label_num']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"📚 Training: {X_train.shape[0]}, Testing: {X_test.shape[0]}")

# Train model
print("\n🚀 Training Random Forest...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Test
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy*100:.2f}%")

# Save model
os.makedirs("models", exist_ok=True)
with open("models/basic_model.pkl", "wb") as f:
    pickle.dump(model, f)
print(f"💾 Saved: models/basic_model.pkl")

# Test prediction
print("\n🔍 TEST PREDICTION:")
sample = X_test.iloc[0:1]
pred_num = model.predict(sample)[0]
pred_label = [k for k, v in label_map.items() if v == pred_num][0]
print(f"Prediction: {pred_label}")
print(f"Actual: {df.iloc[X_test.index[0]]['label']}")

print("\n" + "=" * 60)
print("🎯 TRAINING COMPLETE!")
print("=" * 60)