"""Enhanced base model abstraction layer with advanced features."""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


class FraudDetectionModel(ABC):
    """Abstract base class for fraud detection models with advanced features."""

    def __init__(self, model_name: str, version: str = "1.0"):
        """Initialize the model.
        
        Args:
            model_name: Name/identifier of the model
            version: Version of the model
        """
        self.model_name = model_name
        self.version = version
        self.is_loaded = False
        self.last_loaded_at: Optional[datetime] = None
        self.prediction_count = 0
        self.accuracy_metrics: Dict[str, float] = {}

    @abstractmethod
    def load_model(self) -> bool:
        """Load the model from disk or initialize it.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def predict(
        self,
        features: Dict[str, Any]
    ) -> Tuple[float, float]:
        """Make a fraud prediction.
        
        Args:
            features: Feature dictionary for the transaction
            
        Returns:
            Tuple[float, float]: (risk_score, confidence_score)
                - risk_score: 0.0 to 1.0
                - confidence_score: 0.0 to 1.0
        """
        pass

    @abstractmethod
    def get_explanation(
        self, 
        features: Dict[str, Any],
        risk_score: Optional[float] = None
    ) -> Tuple[List[str], List[str]]:
        """Get explainable AI output for the prediction.
        
        Args:
            features: Feature dictionary
            risk_score: Optional risk score for context
            
        Returns:
            Tuple[List[str], List[str]]: (contributing_factors, recommendations)
        """
        pass

    @abstractmethod
    def get_shap_values(
        self, 
        features: Dict[str, Any]
    ) -> Dict[str, float]:
        """Get SHAP-like feature importance values.
        
        Args:
            features: Feature dictionary
            
        Returns:
            Dict with feature names and their impact scores
        """
        pass

    @abstractmethod
    def retrain(
        self, 
        training_data: List[Dict], 
        labels: List[int]
    ) -> bool:
        """Retrain the model with new data.
        
        Args:
            training_data: List of training examples
            labels: List of labels (0=legitimate, 1=fraudulent)
            
        Returns:
            bool: True if retraining was successful
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive information about the model.
        
        Returns:
            Dict with model metadata, performance, and capabilities
        """
        pass

    def get_fraud_probability(
        self,
        features: Dict[str, Any]
    ) -> float:
        """Get fraud probability (alias for risk score).
        
        Args:
            features: Feature dictionary
            
        Returns:
            float: Fraud probability 0.0 to 1.0
        """
        risk_score, _ = self.predict(features)
        return risk_score

    def classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level based on score.
        
        Args:
            risk_score: Risk score 0.0 to 1.0
            
        Returns:
            str: Risk level (low, medium, high, critical)
        """
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.6:
            return "medium"
        elif risk_score < 0.8:
            return "high"
        else:
            return "critical"

    def classify_fraud_status(self, risk_score: float) -> str:
        """Classify fraud status based on risk score.
        
        Args:
            risk_score: Risk score 0.0 to 1.0
            
        Returns:
            str: Status (legitimate, suspicious, fraudulent)
        """
        if risk_score >= 0.8:
            return "fraudulent"
        elif risk_score >= 0.5:
            return "suspicious"
        else:
            return "legitimate"
