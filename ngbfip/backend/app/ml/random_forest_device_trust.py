from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

class RandomForestDeviceTrust:
    def __init__(self, n_estimators=100):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        self.is_trained = False

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the Random Forest model for device trust classification
        y_train: 1 for trusted, 0 for untrusted
        """
        self.model.fit(X_train, y_train)
        self.is_trained = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict device trust: 1 for trusted, 0 for untrusted
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Get probability scores for device trust
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        return self.model.predict_proba(X)

    def save_model(self, filepath: str):
        joblib.dump(self.model, filepath)

    def load_model(self, filepath: str):
        self.model = joblib.load(filepath)
        self.is_trained = True
