from sklearn.ensemble import IsolationForest
import numpy as np
import joblib

class IsolationForestModel:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_trained = False

    def train(self, X_train: np.ndarray):
        """
        Train the Isolation Forest model
        """
        self.model.fit(X_train)
        self.is_trained = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies: -1 for anomalies, 1 for normal
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        return -self.model.score_samples(X)

    def save_model(self, filepath: str):
        joblib.dump(self.model, filepath)

    def load_model(self, filepath: str):
        self.model = joblib.load(filepath)
        self.is_trained = True
