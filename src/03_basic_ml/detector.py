# File: src/03_basic_ml/detector.py

class SimpleDetector:
    """
    Detect attacks using trained model
    """
    
    def __init__(self, model_path="models/basic_model.pkl"):
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        self.label_map = {
            0: 'normal',
            1: 'brute_force',
            2: 'port_scan',
            3: 'dos'
        }
    
    def detect(self, log_data):
        """
        Detect if log entry is an attack
        """
        # Convert single log to format model expects
        features = self.extract_features(log_data)
        
        # Make prediction
        prediction = self.model.predict([features])[0]
        probability = self.model.predict_proba([features])[0]
        
        result = {
            'prediction': self.label_map[prediction],
            'confidence': max(probability) * 100,
            'is_attack': prediction != 0,
            'details': {
                'prob_normal': probability[0] * 100,
                'prob_brute_force': probability[1] * 100,
                'prob_port_scan': probability[2] * 100,
                'prob_dos': probability[3] * 100
            }
        }
        
        return result
    
    def test_with_sample(self):
        """
        Test with sample attack log
        """
        sample_attack = {
            'src_port': 54321,
            'dst_port': 22,  # SSH port
            'duration': 3500,  # Very long
            'bytes_sent': 500000,
            'bytes_received': 100,
            'hour': 3,  # 3 AM
            'day_of_week': 6,  # Saturday
            'is_weekend': 1,
            'src_ip_numeric': 3405803776,  # 203.0.113.0
            'dst_ip_numeric': 167772161  # 10.0.0.1
        }
        
        result = self.detect(sample_attack)
        print("🔍 Detection Result:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        
        return result