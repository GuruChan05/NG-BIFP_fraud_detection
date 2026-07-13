import numpy as np
from typing import Dict

class RiskFusionEngine:
    def __init__(self):
        self.weights = {
            'transaction_risk': 0.4,
            'device_trust': 0.3,
            'behavioral_anomaly': 0.3
        }

    def calculate_risk_score(
        self,
        transaction_risk: float,
        device_trust_score: float,
        behavioral_anomaly_score: float
    ) -> float:
        """
        Fuse multiple risk signals into a single risk score [0-1]
        """
        risk_score = (
            self.weights['transaction_risk'] * transaction_risk +
            self.weights['device_trust'] * (1 - device_trust_score) +
            self.weights['behavioral_anomaly'] * behavioral_anomaly_score
        )
        return np.clip(risk_score, 0, 1)

    def classify_risk_level(self, risk_score: float) -> str:
        """
        Classify risk into levels: low, medium, high, critical
        """
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.6:
            return "medium"
        elif risk_score < 0.8:
            return "high"
        else:
            return "critical"

    def set_weights(self, weights: Dict[str, float]):
        """
        Update fusion weights
        """
        if sum(weights.values()) != 1.0:
            raise ValueError("Weights must sum to 1.0")
        self.weights = weights
