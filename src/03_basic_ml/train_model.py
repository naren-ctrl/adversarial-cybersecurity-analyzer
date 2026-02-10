# File: src/03_basic_ml/train_model.py

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import pandas as pd
import os
import sys

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../02_preprocessing'))
from clean_data import DataCleaner

class BasicMLTrainer:
    """
    Train a simple machine learning model
    """
    
    def train(self, X, y):
        """
        Train and test a basic model
        """
        print("🤖 Training basic ML model...")
        
        # 1. Split data: 80% for training, 20% for testing
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"Training samples: {X_train.shape[0]}")
        print(f"Testing samples: {X_test.shape[0]}")
        
        # 2. Create model (Random Forest - like many decision trees voting)
        model = RandomForestClassifier(
            n_estimators=100,  # Number of trees
            max_depth=10,      # How deep each tree goes
            random_state=42
        )
        
        # 3. Train the model
        print("Training model... (this might take a minute)")
        model.fit(X_train, y_train)
        
        # 4. Test the model
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"✅ Model Accuracy: {accuracy*100:.2f}%")
        print("\n📊 Detailed Report:")
        print(classification_report(y_test, predictions, 
                                   target_names=list(self.get_label_map().values())))
        
        # 5. Save the model
        os.makedirs("models", exist_ok=True)
        with open("models/basic_model.pkl", "wb") as f:
            pickle.dump(model, f)
        print("💾 Model saved as models/basic_model.pkl")
        
        return model
    
    def get_label_map(self):
        return {
            0: 'normal',
            1: 'brute_force',
            2: 'port_scan',
            3: 'dos'
        }

# Main execution
if __name__ == "__main__":
    # Load data
    df = pd.read_csv("data/raw/sample_logs.csv")
    
    # Clean data
    cleaner = DataCleaner()
    X, y, _ = cleaner.clean_data(df)
    
    # Train model
    trainer = BasicMLTrainer()
    model = trainer.train(X, y)