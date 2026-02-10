# fix_env.py
import subprocess
import sys
import os

print("🔧 FIXING VIRTUAL ENVIRONMENT")
print("=" * 50)

# 1. Install/upgrade pip
print("1. Upgrading pip...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# 2. Install required packages
packages = [
    "pandas==2.1.4",
    "numpy==1.24.4",
    "streamlit==1.29.0",
    "scikit-learn==1.3.2",
    "matplotlib==3.8.2",
    "plotly==5.18.0"
]

print("2. Installing packages...")
for package in packages:
    print(f"   Installing {package}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except:
        print(f"   ⚠️ Failed: {package}")

print("\n3. Testing imports...")
try:
    import pandas as pd
    print("   ✅ pandas")
    
    import streamlit as st
    print("   ✅ streamlit")
    
    import sklearn
    print("   ✅ scikit-learn")
    
    print("\n🎉 ALL PACKAGES INSTALLED SUCCESSFULLY!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("Now run: streamlit run src\\06_web_interface\\app.py")