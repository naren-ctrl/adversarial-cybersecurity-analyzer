# setup_project.py - Save in your main project folder
import os
import pandas as pd
import random
from datetime import datetime, timedelta

print("=" * 60)
print("🛠️  SETUP PROJECT: Creating Sample Data")
print("=" * 60)

# 1. Create sample data
print("📝 Generating cybersecurity logs...")

logs = []
start_time = datetime.now()

# Normal logs (500 for quick testing)
for i in range(500):
    log = {
        "timestamp": (start_time - timedelta(minutes=random.randint(0, 1440))).strftime('%Y-%m-%d %H:%M:%S'),
        "src_ip": f"192.168.{random.randint(1, 5)}.{random.randint(1, 254)}",
        "dst_ip": f"10.0.0.{random.randint(1, 10)}",
        "src_port": random.randint(1024, 65535),
        "dst_port": random.choice([80, 443, 22, 21]),
        "protocol": random.choice(["TCP", "UDP"]),
        "duration": random.randint(1, 60),
        "bytes_sent": random.randint(100, 5000),
        "bytes_received": random.randint(100, 5000),
        "label": "normal"
    }
    logs.append(log)

# Attack logs (50)
for i in range(50):
    attack = random.choice(["brute_force", "port_scan", "dos"])
    
    if attack == "brute_force":
        log = {
            "timestamp": (start_time - timedelta(minutes=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            "src_ip": f"203.0.113.{random.randint(1, 50)}",
            "dst_ip": f"10.0.0.{random.randint(1, 5)}",
            "src_port": random.randint(1024, 65535),
            "dst_port": 22,
            "protocol": "TCP",
            "duration": random.randint(300, 600),
            "bytes_sent": random.randint(50000, 100000),
            "bytes_received": random.randint(10, 100),
            "label": "brute_force"
        }
    elif attack == "port_scan":
        log = {
            "timestamp": (start_time - timedelta(minutes=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            "src_ip": f"198.51.100.{random.randint(1, 50)}",
            "dst_ip": f"10.0.0.{random.randint(1, 10)}",
            "src_port": random.randint(1024, 65535),
            "dst_port": random.choice([21, 22, 23, 3389]),
            "protocol": "TCP",
            "duration": random.randint(1, 5),
            "bytes_sent": random.randint(50, 200),
            "bytes_received": random.randint(0, 50),
            "label": "port_scan"
        }
    else:  # dos
        log = {
            "timestamp": (start_time - timedelta(minutes=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
            "src_ip": f"192.0.2.{random.randint(1, 50)}",
            "dst_ip": f"10.0.0.{random.randint(1, 3)}",
            "src_port": random.randint(1024, 65535),
            "dst_port": 80,
            "protocol": "TCP",
            "duration": random.randint(1, 10),
            "bytes_sent": random.randint(100000, 500000),
            "bytes_received": random.randint(0, 100),
            "label": "dos"
        }
    logs.append(log)

# Save to CSV
df = pd.DataFrame(logs)
df.to_csv("data/raw/sample_logs.csv", index=False)

print(f"✅ Created: data/raw/sample_logs.csv")
print(f"   Total logs: {len(df)}")
print(f"   Normal: {len(df[df['label'] == 'normal'])}")
print(f"   Attacks: {len(df[df['label'] != 'normal'])}")

# Create test file
test_df = df.head(100)
test_df.to_csv("data/raw/test_logs.csv", index=False)
print(f"✅ Created: data/raw/test_logs.csv (100 samples)")

print("\n" + "=" * 60)
print("🎯 SETUP COMPLETE! Run 'python explore_data.py' next")
print("=" * 60)