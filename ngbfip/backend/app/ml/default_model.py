"""Default fraud detection model implementation."""
from typing import Dict, List, Tuple
from .base_model import FraudDetectionModel
import random


class DefaultFraudDetectionModel(FraudDetectionModel):
    """Default fraud detection model using rule-based heuristics.
    
    This is a simple rule-based model that can be replaced with ML models later.
    It provides a baseline for fraud detection.
    """

    def __init__(self):
        super().__init__("default_fraud_detection")
        self.risk_thresholds = {
            "high_amount": 5000,
            "very_high_amount": 20000,
            "medium_amount": 1000,
        }
        self.high_risk_merchants = ["casino", "gambling", "weapons"]
        self.suspicious_countries = ["unknown", "vpn", "proxy"]

    def load_model(self) -> bool:
        """Load the model (no-op for rule-based model)."""
        self.is_loaded = True
        return True

    def predict(self, features: Dict[str, any]) -> Tuple[float, float]:
        """Predict fraud risk using heuristic rules.
        
        Risk factors considered:
        - Amount (higher = higher risk)
        - Merchant category (certain categories = higher risk)
        - Location (suspicious locations = higher risk)
        - Device trust (new/untrusted devices = higher risk)
        - Transaction type (certain types = higher risk)
        """
        risk_score = 0.0
        factors_weight = 0

        # Amount analysis (max 0.35 contribution)
        amount = features.get("amount", 0)
        if amount > self.risk_thresholds["very_high_amount"]:
            risk_score += 0.35
            factors_weight += 1
        elif amount > self.risk_thresholds["high_amount"]:
            risk_score += 0.25
            factors_weight += 0.7
        elif amount > self.risk_thresholds["medium_amount"]:
            risk_score += 0.1
            factors_weight += 0.3

        # Merchant category analysis (max 0.25 contribution)
        merchant_category = features.get("merchant_category", "").lower()
        merchant = features.get("merchant", "").lower()
        if any(high_risk in merchant_category or high_risk in merchant 
               for high_risk in self.high_risk_merchants):
            risk_score += 0.25
            factors_weight += 1

        # Location analysis (max 0.2 contribution)
        location = features.get("location", "").lower()
        if any(suspicious in location for suspicious in self.suspicious_countries):
            risk_score += 0.2
            factors_weight += 1
        elif "international" in location:
            risk_score += 0.1
            factors_weight += 0.5

        # Device trust (max 0.15 contribution)
        is_trusted_device = features.get("is_trusted_device", True)
        if not is_trusted_device:
            risk_score += 0.15
            factors_weight += 1

        # Transaction type analysis (max 0.05 contribution)
        transaction_type = features.get("transaction_type", "").lower()
        if transaction_type == "transfer":
            risk_score += 0.05
            factors_weight += 0.3

        # Normalize risk score to 0-1 range
        risk_score = min(risk_score, 1.0)

        # Confidence score based on number of factors
        confidence = min(0.5 + (factors_weight * 0.1), 1.0)

        return risk_score, confidence

    def get_explanation(
        self, features: Dict[str, any]
    ) -> Tuple[List[str], List[str]]:
        """Get explanation for the prediction."""
        contributing_factors = []
        recommendations = []

        amount = features.get("amount", 0)
        if amount > self.risk_thresholds["very_high_amount"]:
            contributing_factors.append(f"Very high transaction amount (${amount:,.2f})")
            recommendations.append("Verify customer identity before processing")
        elif amount > self.risk_thresholds["high_amount"]:
            contributing_factors.append(f"High transaction amount (${amount:,.2f})")
            recommendations.append("Request additional verification")

        merchant_category = features.get("merchant_category", "").lower()
        merchant = features.get("merchant", "").lower()
        if any(high_risk in merchant_category or high_risk in merchant
               for high_risk in self.high_risk_merchants):
            contributing_factors.append(f"High-risk merchant category: {merchant}")
            recommendations.append("Flag for manual review")

        location = features.get("location", "").lower()
        if any(suspicious in location for suspicious in self.suspicious_countries):
            contributing_factors.append(f"Suspicious location: {location}")
            recommendations.append("Verify location authenticity")

        is_trusted_device = features.get("is_trusted_device", True)
        if not is_trusted_device:
            contributing_factors.append("Transaction from untrusted/new device")
            recommendations.append("Send verification code to registered email")

        if not contributing_factors:
            contributing_factors.append("No significant risk factors detected")
            recommendations.append("Process transaction normally")

        return contributing_factors, recommendations

    def retrain(self, training_data: List[Dict], labels: List[int]) -> bool:
        """Retrain the model (not applicable for rule-based model)."""
        # For now, rule-based model doesn't need retraining
        # This would be implemented for ML-based models
        return True

    def get_model_info(self) -> Dict[str, any]:
        """Get model information."""
        return {
            "name": self.model_name,
            "type": "rule_based",
            "version": "1.0",
            "description": "Rule-based fraud detection model using heuristics",
            "is_loaded": self.is_loaded,
        }
