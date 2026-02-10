# explore_data.py - Save in main project folder
import pandas as pd
import matplotlib.pyplot as plt
import os

print("=" * 60)
print("🔍 EXPLORING CYBERSECURITY DATA")
print("=" * 60)

# Load data
file_path = "data/raw/sample_logs.csv"
if not os.path.exists(file_path):
    print(f"❌ ERROR: {file_path} not found!")
    print("💡 Run 'python setup_project.py' first!")
    exit()

df = pd.read_csv(file_path)
print(f"✅ Loaded {len(df)} logs from {file_path}")

# Basic info
print(f"\n📊 Data Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n📋 Columns: {', '.join(df.columns.tolist())}")

# Threat distribution
print("\n⚠️  THREAT DISTRIBUTION:")
threat_counts = df['label'].value_counts()
for label, count in threat_counts.items():
    percent = (count / len(df)) * 100
    print(f"   {label:15} : {count:4} ({percent:.1f}%)")

# Simple plot
plt.figure(figsize=(8, 4))
colors = ['green' if label == 'normal' else 'red' for label in threat_counts.index]
plt.bar(threat_counts.index, threat_counts.values, color=colors)
plt.title('Log Distribution')
plt.xlabel('Log Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('results/threat_distribution.png')
plt.show()

print(f"\n💾 Saved: results/threat_distribution.png")

# Show sample
print("\n🔍 SAMPLE DATA (First 3 rows):")
print(df.head(3))

print("\n" + "=" * 60)
print("✅ EXPLORATION COMPLETE!")
print("=" * 60)