"""Base model abstraction layer for fraud detection."""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from pydantic import BaseModel


class FraudDetectionModel(ABC):
    """Abstract base class for fraud detection models."""

    def __init__(self, model_name: str):
        """Initialize the model.
        
        Args:
            model_name: Name/identifier of the model
        """
        self.model_name = model_name
        self.is_loaded = False

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
        features: Dict[str, any]
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
    def get_explanation(self, features: Dict[str, any]) -> Tuple[List[str], List[str]]:
        """Get explanation for the prediction.
        
        Args:
            features: Feature dictionary
            
        Returns:
            Tuple[List[str], List[str]]: (contributing_factors, recommendations)
        """
        pass

    @abstractmethod
    def retrain(self, training_data: List[Dict], labels: List[int]) -> bool:
        """Retrain the model with new data.
        
        Args:
            training_data: List of training examples
            labels: List of labels (0=legitimate, 1=fraudulent)
            
        Returns:
            bool: True if retraining was successful
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, any]:
        """Get information about the model.
        
        Returns:
            Dict with model metadata
        """
        pass
