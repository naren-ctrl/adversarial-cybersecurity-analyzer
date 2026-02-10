import pandas as pd
import requests
import zipfile
import os
import random
from datetime import datetime, timedelta
import numpy as np

class DataCollector:
    def __init__(self):
        print("🚀 Starting data collection...")
        
    def create_sample_logs(self):
        """
        Create simple practice logs for beginners
        """
        print("📝 Creating sample log data for practice...")
        
        # Create directories if they don't exist
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("data/adversarial_samples", exist_ok=True)
        
        logs = []
        start_time = datetime.now()
        
        # Generate 1000 normal logs
        for i in range(1000):
            log = {
                "timestamp": (start_time + timedelta(seconds=i*10)).strftime('%Y-%m-%d %H:%M:%S'),
                "src_ip": f"192.168.1.{random.randint(1, 50)}",
                "dst_ip": f"10.0.0.{random.randint(1, 10)}",
                "src_port": random.randint(1024, 65535),
                "dst_port": random.choice([80, 443, 22, 21]),
                "protocol": random.choice(["TCP", "UDP"]),
                "duration": random.randint(1, 60),
                "bytes_sent": random.randint(100, 10000),
                "bytes_received": random.randint(100, 5000),
                "label": "normal"  # This log is normal
            }
            logs.append(log)
        
        # Generate 50 attack logs
        attacks = ["brute_force", "port_scan", "dos"]
        for i in range(50):
            log = {
                "timestamp": (start_time + timedelta(seconds=10000 + i*5)).strftime('%Y-%m-%d %H:%M:%S'),
                "src_ip": f"203.0.113.{random.randint(1, 10)}",  # Different IP range
                "dst_ip": f"10.0.0.{random.randint(1, 10)}",
                "src_port": random.randint(1024, 65535),
                "dst_port": random.choice([22, 23, 3389]),  # Suspicious ports
                "protocol": "TCP",
                "duration": random.randint(300, 3600),  # Long duration
                "bytes_sent": random.randint(100000, 1000000),  # Large data
                "bytes_received": random.randint(100, 1000),
                "label": random.choice(attacks)  # This is an attack
            }
            logs.append(log)
        
        # Save to CSV
        df = pd.DataFrame(logs)
        df.to_csv("data/raw/sample_logs.csv", index=False)
        print(f"✅ Created {len(logs)} sample logs in data/raw/sample_logs.csv")
        
        # Also create a smaller test file
        df.head(100).to_csv("data/raw/test_logs.csv", index=False)
        print(f"✅ Created test file with 100 logs: data/raw/test_logs.csv")
        
        return df
    
    def ip_to_number(self, ip):
        """
        Convert IP like '192.168.1.1' to a number
        """
        try:
            parts = ip.split('.')
            if len(parts) == 4:
                return (int(parts[0]) * 256**3 + 
                        int(parts[1]) * 256**2 + 
                        int(parts[2]) * 256 + 
                        int(parts[3]))
            return 0
        except:
            return 0

# Run this
if __name__ == "__main__":
    print("=" * 50)
    print("ADVERSARIAL CYBERSECURITY DATA COLLECTOR")
    print("=" * 50)
    
    collector = DataCollector()
    
    try:
        # Create sample data
        data = collector.create_sample_logs()
        
        print("\n📊 Sample of your data:")
        print("-" * 50)
        print(data.head())
        
        print("\n📈 Data Statistics:")
        print("-" * 50)
        print(f"Total logs: {len(data)}")
        print(f"Normal logs: {len(data[data['label'] == 'normal'])}")
        print(f"Attack logs: {len(data[data['label'] != 'normal'])}")
        
        print("\n🔍 Attack Distribution:")
        print("-" * 50)
        attack_counts = data[data['label'] != 'normal']['label'].value_counts()
        for attack, count in attack_counts.items():
            print(f"{attack}: {count}")
        
        print("\n✅ Data collection completed successfully!")
        print("📁 Check the 'data/raw' folder for your log files")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("\n💡 Troubleshooting steps:")
        print("1. Check if you have write permissions")
        print("2. Make sure Python is installed correctly")
        print("3. Try creating the folder manually:")
        print("   mkdir data")
        print("   mkdir data\\raw")