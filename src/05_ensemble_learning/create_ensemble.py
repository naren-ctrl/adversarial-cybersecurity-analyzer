# File: src/05_ensemble_learning/create_ensemble.py

import os
import sys
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier

# Ensure adversarial detector can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../04_adversarial_defense'))
from detector import AdversarialDetector


class ModelEnsemble:
    """
    Create a team of different ML models
    """
    
    def __init__(self):
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100),
            'xgboost': XGBClassifier(n_estimators=100, learning_rate=0.1),
            'svm': SVC(probability=True),
            'neural_net': MLPClassifier(hidden_layer_sizes=(64, 32))
        }
        
        self.adversarial_detector = AdversarialDetector()
    
    def train_ensemble(self, X_train, y_train):
        """
        Train all models in the ensemble
        """
        print("👥 Training ensemble of models...")
        
        trained_models = {}
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            trained_models[name] = model
        
        # Save all models
        os.makedirs("models/ensemble", exist_ok=True)
        for name, model in trained_models.items():
            with open(f"models/ensemble/{name}.pkl", "wb") as f:
                pickle.dump(model, f)
        
        print("✅ All ensemble models trained and saved")
        return trained_models
    
    def predict_with_ensemble(self, log_features):
        """
        Get predictions from all models
        """
        if not self.models:
            print("⚠️  No models available for prediction!")
            return {
                'individual_predictions': {},
                'individual_probabilities': {},
                'agreement_level': 0.0,
                'final_prediction': 0,
                'model_disagreement': False,
                'error': 'No models available'
            }
        
        predictions = {}
        probabilities = {}
        
        for name, model in self.models.items():
            try:
                pred = model.predict([log_features])[0]
                prob = model.predict_proba([log_features])[0]
                
                predictions[name] = pred
                probabilities[name] = prob
            except Exception as e:
                print(f"⚠️ Model {name} failed to predict: {e}")
                continue
        
        # If no successful predictions, return default safe result
        if not predictions:
            print("⚠️  No successful predictions from any model!")
            return {
                'individual_predictions': {},
                'individual_probabilities': {},
                'agreement_level': 0.0,
                'final_prediction': 0,
                'model_disagreement': False,
                'error': 'No successful predictions'
            }
        
        # Check for disagreements (might indicate adversarial attack)
        unique_predictions = set(predictions.values())
        
        agreement = self.calculate_agreement(predictions)
        combined = self.combine_predictions(predictions, probabilities)
        
        result = {
            'individual_predictions': predictions,
            'individual_probabilities': probabilities,
            'agreement_level': agreement,
            'final_prediction': combined,
            'model_disagreement': len(unique_predictions) > 1
        }
        
        # If models disagree, check for adversarial attack
        if result['model_disagreement']:
            try:
                adv_check = self.adversarial_detector.detect(log_features, result)
                result['adversarial_check'] = adv_check
            except Exception as e:
                print(f"⚠️ Adversarial detection failed: {e}")
        
        return result
    
    def calculate_agreement(self, predictions):
        """
        Calculate how much models agree
        """
        from collections import Counter
        
        if not predictions:
            return 0.0
        
        counts = Counter(predictions.values())
        most_common_result = counts.most_common(1)
        
        if not most_common_result:
            return 0.0
        
        most_common = most_common_result[0][1]
        return most_common / len(predictions)
    
    def combine_predictions(self, predictions, probabilities):
        """
        Combine all model predictions (like voting)
        """
        from collections import Counter
        
        if not predictions:
            return 0  # Default to normal if no predictions
        
        most_common_result = Counter(predictions.values()).most_common(1)
        
        if not most_common_result:
            return 0
        
        final = most_common_result[0][0]
        return final