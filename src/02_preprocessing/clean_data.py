# File: src/02_preprocessing/clean_data.py

import pandas as pd


class DataCleaner:
    """
    Clean and prepare log data for machine learning
    """
    
    def __init__(self):
        self.label_map = {
            'normal': 0,
            'brute_force': 1,
            'port_scan': 2,
            'dos': 3
        }
    
    def clean_data(self, df):
        """
        Step-by-step data cleaning
        """
        print("🧹 Cleaning data...")
        
        # 1. Check for missing values
        print(f"Missing values before: {df.isnull().sum().sum()}")
        df = df.dropna()  # Remove rows with missing values
        print(f"Missing values after: {df.isnull().sum().sum()}")
        
        # 2. Convert timestamp to useful features
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        
        # 3. Convert IP addresses to numbers (simplified)
        df['src_ip_numeric'] = df['src_ip'].apply(self.ip_to_number)
        df['dst_ip_numeric'] = df['dst_ip'].apply(self.ip_to_number)
        
        # 4. Convert labels to numbers
        df['label_encoded'] = df['label'].map(self.label_map)
        
        # 5. Select features for ML
        features = [
            'src_port', 'dst_port', 'duration',
            'bytes_sent', 'bytes_received',
            'hour', 'day_of_week', 'is_weekend',
            'src_ip_numeric', 'dst_ip_numeric'
        ]
        
        X = df[features]  # Features (what we look at)
        y = df['label_encoded']  # Labels (what we predict)
        
        print(f"✅ Cleaned data: {X.shape[0]} samples, {X.shape[1]} features")
        return X, y, df
    
    def ip_to_number(self, ip):
        """
        Convert IP like '192.168.1.1' to a number
        """
        parts = ip.split('.')
        if len(parts) == 4:
            return (int(parts[0]) * 256**3 + 
                    int(parts[1]) * 256**2 + 
                    int(parts[2]) * 256 + 
                    int(parts[3]))
        return 0

    def extract_features_single(self, raw_log):
        """Create feature vector from a single raw log dict"""
        # Parse timestamp
        hour = 12
        day_of_week = 0
        is_weekend = 0
        ts = raw_log.get('timestamp')
        try:
            if ts:
                dt = pd.to_datetime(ts)
                hour = int(dt.hour)
                day_of_week = int(dt.dayofweek)
                is_weekend = 1 if day_of_week >= 5 else 0
        except Exception:
            pass

        src_ip_num = self.ip_to_number(raw_log.get('src_ip', '0.0.0.0'))
        dst_ip_num = self.ip_to_number(raw_log.get('dst_ip', '0.0.0.0'))

        features = [
            int(raw_log.get('src_port', 0)),
            int(raw_log.get('dst_port', 0)),
            float(raw_log.get('duration', 0)),
            float(raw_log.get('bytes_sent', 0)),
            float(raw_log.get('bytes_received', 0)),
            hour,
            day_of_week,
            is_weekend,
            src_ip_num,
            dst_ip_num
        ]

        # Return as plain list to pass into sklearn predict methods
        return features