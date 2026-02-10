# test_detection.py - Save in main project folder
import pickle
import pandas as pd
import numpy as np

print("=" * 60)
print("🔍 TESTING THREAT DETECTION")
print("=" * 60)

# Load model
with open("models/basic_model.pkl", "rb") as f:
    model = pickle.load(f)
print("✅ Model loaded")

# Label mapping
label_map = {0: 'normal', 1: 'brute_force', 2: 'port_scan', 3: 'dos'}

def ip_to_number(ip):
    try:
        parts = ip.split('.')
        return sum(int(part) * (256 ** (3-i)) for i, part in enumerate(parts))
    except:
        return 0

# Test cases
test_cases = [
    # Normal traffic
    {
        'src_ip': '192.168.1.10',
        'dst_ip': '10.0.0.1',
        'src_port': 54321,
        'dst_port': 80,
        'duration': 30,
        'bytes_sent': 1500,
        'bytes_received': 7500
    },
    # Brute force attack
    {
        'src_ip': '203.0.113.5',
        'dst_ip': '10.0.0.5',
        'src_port': 12345,
        'dst_port': 22,
        'duration': 500,
        'bytes_sent': 75000,
        'bytes_received': 50
    },
    # Port scan
    {
        'src_ip': '198.51.100.10',
        'dst_ip': '10.0.0.2',
        'src_port': 23456,
        'dst_port': 3389,
        'duration': 2,
        'bytes_sent': 100,
        'bytes_received': 10
    }
]

print("\n🧪 RUNNING DETECTION TESTS:")
print("-" * 40)

for i, test in enumerate(test_cases, 1):
    # Prepare features
    features = np.array([[
        test['src_port'],
        test['dst_port'],
        test['duration'],
        test['bytes_sent'],
        test['bytes_received'],
        ip_to_number(test['src_ip']),
        ip_to_number(test['dst_ip'])
    ]])
    
    # Predict
    pred_num = model.predict(features)[0]
    pred_label = label_map[pred_num]
    
    # Get probabilities
    probs = model.predict_proba(features)[0]
    
    print(f"\nTest {i}:")
    print(f"  From: {test['src_ip']}:{test['src_port']}")
    print(f"  To: {test['dst_ip']}:{test['dst_port']}")
    print(f"  Duration: {test['duration']}s, Bytes: {test['bytes_sent']:,} sent")
    print(f"  🔍 Detection: {pred_label}")
    print(f"  📊 Confidence: {max(probs)*100:.1f}%")
    
    if pred_label != 'normal':
        print(f"  ⚠️  THREAT DETECTED: {pred_label}")

print("\n" + "=" * 60)
print("✅ DETECTION TESTING COMPLETE!")
print("=" * 60)