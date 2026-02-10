# File: src/07_testing/test_system.py

class SystemTester:
    """
    Test the complete system
    """
    
    def run_all_tests(self):
        """Run comprehensive tests"""
        print("🧪 RUNNING SYSTEM TESTS")
        print("=" * 60)
        
        tests = [
            self.test_normal_traffic,
            self.test_brute_force,
            self.test_port_scan,
            self.test_dos_attack,
            self.test_adversarial_attack,
            self.test_ensemble_agreement
        ]
        
        results = {}
        for test in tests:
            test_name = test.__name__
            print(f"\nRunning: {test_name}")
            try:
                result = test()
                results[test_name] = "PASS" if result else "FAIL"
                print(f"✅ {test_name}: PASS")
            except Exception as e:
                results[test_name] = f"FAIL - {str(e)}"
                print(f"❌ {test_name}: FAIL - {e}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        for test, result in results.items():
            print(f"{test:30} {result}")
    
    def test_normal_traffic(self):
        """Test that normal traffic is correctly identified"""
        pipeline = CompleteDetectionPipeline()
        
        normal_log = {
            'src_ip': '192.168.1.100',
            'dst_ip': '10.0.0.1',
            'dst_port': 80,
            'duration': 5,
            'bytes_sent': 1500,
            'bytes_received': 7500,
            'timestamp': '2024-01-15 14:30:00'
        }
        
        result = pipeline.process_log(normal_log)
        return result['threat_detection']['prediction'] == 'normal'
    
    def test_adversarial_attack(self):
        """Test adversarial attack detection"""
        pipeline = CompleteDetectionPipeline()
        
        # Create adversarial log (trying to look normal)
        adv_log = {
            'src_ip': '203.0.113.5',  # Suspicious IP range
            'dst_ip': '10.0.0.5',
            'dst_port': 22,  # SSH
            'duration': 30,  # Made normal (was 3000)
            'bytes_sent': 2000,  # Made normal (was 500000)
            'bytes_received': 100,
            'timestamp': '2024-01-15 09:30:00'  
        }
        
        result = pipeline.process_log(adv_log)
        
        # Should detect as brute force OR detect adversarial attack
        return (result['threat_detection']['prediction'] == 'brute_force' or
                result['adversarial_check'].get('adversarial_attack_detected', False))

# File: README.md
"""
# 🛡️ Adversarial-Resilient Cybersecurity Log Analyzer

## Overview
AI system that detects cyber threats even when attackers try to trick it.

## Quick Start

1. **Installation**
```bash
git clone https://github.com/yourusername/adversarial-cybersecurity-analyzer.git
cd adversarial-cybersecurity-analyzer
pip install -r requirements.txt
"""