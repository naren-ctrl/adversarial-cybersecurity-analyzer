# File: src/05_ensemble_learning/full_pipeline.py

import os
import sys
import pickle
import pandas as pd

# Ensure preprocessing utilities are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../02_preprocessing'))
from clean_data import DataCleaner

from create_ensemble import ModelEnsemble
from risk_scorer import RiskScorer


class CompleteDetectionPipeline:
    """
    Complete system from log input to risk score
    """
    
    def __init__(self):
        self.data_cleaner = DataCleaner()
        self.ensemble = ModelEnsemble()
        self.risk_scorer = RiskScorer()
        
        # Load trained models
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        self.models = {}
        # Construct path relative to project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        models_dir = os.path.join(project_root, "models", "ensemble")
        
        print(f"🔍 Looking for models in: {models_dir}")
        
        # Create directory if it doesn't exist
        if not os.path.exists(models_dir):
            os.makedirs(models_dir, exist_ok=True)
            print(f"📁 Created models directory: {models_dir}")
        
        # Load models if they exist
        ensemble_files = [f for f in os.listdir(models_dir) if f.endswith(".pkl")]
        print(f"🔍 Found {len(ensemble_files)} ensemble models")
        
        for model_file in ensemble_files:
            name = model_file[:-4]
            try:
                with open(os.path.join(models_dir, model_file), "rb") as f:
                    self.models[name] = pickle.load(f)
                print(f"✅ Loaded ensemble model: {name}")
            except Exception as e:
                print(f"⚠️  Failed to load {model_file}: {e}")
        
        # If no models found, use basic_model as fallback
        if not self.models:
            basic_model_path = os.path.join(project_root, "models", "basic_model.pkl")
            print(f"🔍 No ensemble models found. Checking for basic_model at: {basic_model_path}")
            if os.path.exists(basic_model_path):
                try:
                    with open(basic_model_path, "rb") as f:
                        self.models["basic_model"] = pickle.load(f)
                    print(f"✅ Loaded fallback basic_model")
                except Exception as e:
                    print(f"⚠️  Failed to load basic_model: {e}")
                    print("⚠️  Loading without pre-trained models (will require training)")
            else:
                print(f"⚠️  Model file not found at {basic_model_path}")
        
        print(f"📊 Total models loaded: {len(self.models)}")
        print(f"📊 Model names: {list(self.models.keys())}")
        
        self.ensemble.models = self.models
    
    def process_log(self, raw_log):
        """
        Complete processing of a single log
        """
        print(f"\n🔍 Processing log from {raw_log.get('src_ip', 'unknown')}")
        print("-" * 50)
        
        # Step 1: Clean and extract features
        features = self.data_cleaner.extract_features_single(raw_log)
        
        # Step 2: Ensemble prediction
        ensemble_result = self.ensemble.predict_with_ensemble(features)
        
        # Step 3: Get context
        context = self.get_context(raw_log)
        
        # Step 4: Calculate risk
        risk_result = self.risk_scorer.calculate_risk_score(
            {
                'prediction': self.get_label(ensemble_result['final_prediction']),
                'confidence': ensemble_result.get('agreement_level', 0.5) * 100,
                'adversarial_attack_detected': ensemble_result.get('adversarial_check', {}).get('adversarial_attack_detected', False)
            },
            context
        )
        
        # Step 5: Prepare final result
        final_result = {
            'timestamp': raw_log.get('timestamp', 'unknown'),
            'source_ip': raw_log.get('src_ip', 'unknown'),
            'destination': f"{raw_log.get('dst_ip', 'unknown')}:{raw_log.get('dst_port', 'unknown')}",
            'threat_detection': {
                'prediction': self.get_label(ensemble_result['final_prediction']),
                'confidence': f"{ensemble_result.get('agreement_level', 0) * 100:.1f}%",
                'model_agreement': f"{ensemble_result.get('agreement_level', 0) * 100:.1f}%"
            },
            'adversarial_check': ensemble_result.get('adversarial_check', {}),
            'risk_assessment': risk_result,
            'raw_features': features
        }
        
        # Display result
        self.display_result(final_result)
        
        return final_result
    
    def get_label(self, encoded):
        """Convert encoded label to name"""
        label_map = {0: 'normal', 1: 'brute_force', 2: 'port_scan', 3: 'dos'}
        return label_map.get(encoded, 'unknown')
    
    def get_context(self, log):
        """Extract context information"""
        context = {}
        
        hour = pd.to_datetime(log.get('timestamp', '')).hour if log.get('timestamp') else 12
        if 9 <= hour <= 17:
            context['business_hours'] = True
        else:
            context['after_hours'] = True
        
        # Check if targeting critical ports
        critical_ports = [22, 3389, 1433, 1521]  # SSH, RDP, SQL
        if log.get('dst_port') in critical_ports:
            context['target_critical'] = True
        
        return context
    
    def display_result(self, result):
        """Display result in readable format"""
        print(f"\n📊 RESULT")
        print(f"Threat: {result['threat_detection']['prediction']}")
        print(f"Confidence: {result['threat_detection']['confidence']}")
        
        if result['adversarial_check'].get('adversarial_attack_detected'):
            print(f"🚨 ADVERSARIAL ATTACK DETECTED!")
            for alert in result['adversarial_check'].get('alerts', []):
                print(f"   - {alert['type']} (Confidence: {alert['confidence']}%)")
        
        print(f"\n⚠️  RISK ASSESSMENT")
        print(f"Risk Score: {result['risk_assessment']['risk_score']}/100")
        print(f"Risk Level: {result['risk_assessment']['risk_level']}")
        print(f"Action: {result['risk_assessment']['recommended_action']}")
        print("=" * 50)