# File: src/04_adversarial_defense/create_attacks.py

import numpy as np

class AdversarialAttackCreator:
    """
    Create fake logs that try to fool ML models
    """
    
    def __init__(self, original_model):
        self.model = original_model
    
    def create_evasion_attack(self, original_log):
        """
        Modify a brute force attack to look normal
        """
        print("🎭 Creating evasion attack...")
        
        # Copy original log
        adversarial_log = original_log.copy()
        
        # Attack strategy 1: Make duration normal
        if original_log['duration'] > 300:  # If too long
            adversarial_log['duration'] = np.random.randint(1, 60)
        
        # Attack strategy 2: Make bytes sent normal
        if original_log['bytes_sent'] > 100000:
            adversarial_log['bytes_sent'] = np.random.randint(100, 10000)
        
        # Attack strategy 3: Change timing
        if original_log['hour'] == 3:  # Suspicious 3 AM
            adversarial_log['hour'] = np.random.randint(9, 17)  # Business hours
        
        print(f"Original log was {self.detect(original_log)}")
        print(f"Adversarial log is {self.detect(adversarial_log)}")
        
        return adversarial_log
    
    def create_poisoning_attack(self, training_data, num_poison=10):
        """
        Add fake 'normal' logs that are actually attacks
        """
        print("☠️ Creating data poisoning attack...")
        
        poisoned_data = training_data.copy()
        
        for i in range(num_poison):
            # Create log that looks normal but has attack patterns
            poisoned_log = {
                'src_port': np.random.randint(1024, 65535),
                'dst_port': 22,  # SSH
                'duration': np.random.randint(1, 60),  # Looks normal
                'bytes_sent': np.random.randint(100, 5000),  # Looks normal
                'bytes_received': np.random.randint(100, 1000),
                'hour': np.random.randint(9, 17),  # Business hours
                'day_of_week': np.random.randint(0, 5),  # Weekday
                'is_weekend': 0,
                'src_ip_numeric': self.ip_to_number(f"203.0.113.{i}"),  # Suspicious IP range
                'dst_ip_numeric': self.ip_to_number("10.0.0.5"),
                'label': 'normal'  # But labeled as normal!
            }
            
            poisoned_data = poisoned_data.append(poisoned_log, ignore_index=True)
        
        print(f"Added {num_poison} poisoned samples")
        return poisoned_data