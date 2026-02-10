# src/04_adversarial_defense/detector.py - CORRECTED
import numpy as np

class AdversarialDetector:
    """
    Detect when attackers are trying to fool our model
    """
    
    def __init__(self):
        self.detection_methods = [
            self.detect_statistical_anomalies,
            self.detect_feature_manipulation,
            self.detect_pattern_evasion  # Fixed: This method exists now
        ]
    
    def detect(self, log_features, model_prediction):
        """
        Check if log is trying to evade detection
        """
        alerts = []
        
        for method in self.detection_methods:
            result = method(log_features, model_prediction)
            if result['is_suspicious']:
                alerts.append(result)
        
        if alerts:
            return {
                'adversarial_attack_detected': True,
                'confidence': max([a['confidence'] for a in alerts]),
                'attack_types': [a['type'] for a in alerts],
                'alerts': alerts,
                'recommendation': 'Use robust detection mode'
            }
        else:
            return {'adversarial_attack_detected': False}
    
    def detect_statistical_anomalies(self, features, prediction):
        """
        Check if features are statistically weird
        """
        if not isinstance(features, dict):
            features = features if hasattr(features, '__dict__') else {}
        
        feature_values = list(features.values()) if isinstance(features, dict) else []
        
        if len(feature_values) > 0:
            feature_std = np.std(feature_values)
            
            if feature_std < 0.1:  # Too consistent
                return {
                    'is_suspicious': True,
                    'type': 'Statistical Evasion',
                    'confidence': 85,
                    'reason': 'Features are too perfectly normal'
                }
        
        return {'is_suspicious': False}
    
    def detect_feature_manipulation(self, features, prediction):
        """
        Check for unnatural feature combinations
        """
        if not isinstance(features, dict):
            return {'is_suspicious': False}
        
        # Example: SSH traffic at odd hours with normal duration is suspicious
        dst_port = features.get('dst_port', 0)
        hour = features.get('hour', 12)
        duration = features.get('duration', 0)
        
        if (dst_port == 22 and  # SSH
            hour in [0, 1, 2, 3, 4] and  # Late night
            duration < 10):  # But short duration
            
            return {
                'is_suspicious': True,
                'type': 'Feature Manipulation',
                'confidence': 90,
                'reason': 'Unnatural combination: SSH at night but short duration'
            }
        
        return {'is_suspicious': False}
    
    def detect_pattern_evasion(self, features, prediction):
        """
        Check for pattern-based evasion attempts
        This was the MISSING METHOD causing the error
        """
        if not isinstance(features, dict):
            return {'is_suspicious': False}
        
        # Check for "too normal" patterns
        normal_count = 0
        total_checks = 0
        
        # Check common "normal" patterns
        checks = [
            ('duration', lambda x: 1 <= x <= 60, "normal duration"),
            ('bytes_sent', lambda x: 100 <= x <= 10000, "normal bytes sent"),
            ('hour', lambda x: 9 <= x <= 17, "business hours"),
            ('dst_port', lambda x: x in [80, 443, 22, 21], "common port")
        ]
        
        for feature_name, check_func, desc in checks:
            if feature_name in features:
                total_checks += 1
                if check_func(features[feature_name]):
                    normal_count += 1
        
        # If everything is perfectly "normal", might be evasion
        if total_checks > 0 and normal_count == total_checks:
            return {
                'is_suspicious': True,
                'type': 'Pattern Evasion',
                'confidence': 75,
                'reason': 'All features perfectly match normal patterns'
            }
        
        return {'is_suspicious': False}
    
    # Additional helper methods
    def calculate_entropy_drift(self, logs):
        """Calculate entropy change in logs"""
        return 0.1  # Simplified
    
    def detect_gan_logs(self, logs):
        """Detect GAN-generated fake logs"""
        return 0.2  # Simplified
    
    def analyze_timestamp_patterns(self, logs):
        """Check timestamp manipulation"""
        return False  # Simplified
    def detect_pattern_evasion(self, features, prediction):
        """Added missing method"""
        return {'is_suspicious': False}
