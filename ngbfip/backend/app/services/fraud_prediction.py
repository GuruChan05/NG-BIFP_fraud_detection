"""Fraud prediction service."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import json
from app.db.models.fraud_prediction import FraudPrediction
from app.db.models.transaction import Transaction
from app.ml.default_model import DefaultFraudDetectionModel
from app.schemas.fraud_prediction import FraudPredictionRequest


class FraudPredictionService:
    """Service for fraud prediction and management."""

    def __init__(self):
        """Initialize the fraud prediction service."""
        self.model = DefaultFraudDetectionModel()
        self.model.load_model()

    def predict(
        self,
        db: Session,
        prediction_request: FraudPredictionRequest,
        transaction_id: Optional[int] = None,
    ) -> FraudPrediction:
        """Make a fraud prediction for a transaction.
        
        Args:
            db: Database session
            prediction_request: Prediction request data
            transaction_id: Optional transaction ID if updating existing transaction
            
        Returns:
            FraudPrediction: Stored prediction result
        """
        # Prepare features for the model
        features = {
            "amount": prediction_request.amount,
            "transaction_type": prediction_request.transaction_type,
            "merchant": prediction_request.merchant,
            "merchant_category": prediction_request.merchant_category,
            "location": prediction_request.location,
            "device_id": prediction_request.device_id,
            "is_trusted_device": self._is_trusted_device(db, prediction_request.device_id),
        }

        # Get prediction from model
        risk_score, confidence_score = self.model.predict(features)

        # Get explanation
        contributing_factors, recommendations = self.model.get_explanation(features)

        # Determine fraud status
        is_fraudulent = self._classify_fraud_status(risk_score)
        risk_level = self._get_risk_level(risk_score)

        # Create prediction record
        prediction = FraudPrediction(
            user_id=prediction_request.user_id,
            transaction_id=transaction_id,
            risk_score=risk_score,
            confidence_score=confidence_score,
            is_fraudulent=is_fraudulent,
            risk_level=risk_level,
            explanation=self._generate_explanation(risk_score, is_fraudulent),
            contributing_factors=json.dumps(contributing_factors),
            recommendations=json.dumps(recommendations),
            model_name=self.model.model_name,
            model_version="1.0",
        )

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return prediction

    def get_prediction(db: Session, prediction_id: int) -> Optional[FraudPrediction]:
        """Get a specific prediction."""
        return db.query(FraudPrediction).filter(
            FraudPrediction.id == prediction_id
        ).first()

    def get_user_prediction_history(
        self,
        db: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[FraudPrediction], int]:
        """Get prediction history for a user."""
        query = db.query(FraudPrediction).filter(
            FraudPrediction.user_id == user_id
        ).order_by(FraudPrediction.created_at.desc())

        total = query.count()
        skip = (page - 1) * page_size
        predictions = query.offset(skip).limit(page_size).all()

        return predictions, total

    def get_statistics(self, db: Session) -> Dict[str, any]:
        """Get fraud prediction statistics."""
        total_predictions = db.query(func.count(FraudPrediction.id)).scalar() or 0
        fraudulent_count = db.query(func.count(FraudPrediction.id)).filter(
            FraudPrediction.is_fraudulent == "fraudulent"
        ).scalar() or 0
        average_risk = db.query(func.avg(FraudPrediction.risk_score)).scalar() or 0.0
        average_confidence = db.query(func.avg(FraudPrediction.confidence_score)).scalar() or 0.0

        return {
            "total_predictions": total_predictions,
            "fraudulent_count": fraudulent_count,
            "fraud_percentage": (fraudulent_count / total_predictions * 100) if total_predictions > 0 else 0,
            "average_risk_score": round(average_risk, 3),
            "average_confidence_score": round(average_confidence, 3),
        }

    @staticmethod
    def _is_trusted_device(db: Session, device_id: Optional[str]) -> bool:
        """Check if a device is trusted."""
        if not device_id:
            return True

        from app.db.models.device import Device
        device = db.query(Device).filter(
            Device.id == device_id
        ).first()
        return device.is_trusted if device else False

    @staticmethod
    def _classify_fraud_status(risk_score: float) -> str:
        """Classify fraud status based on risk score."""
        if risk_score >= 0.8:
            return "fraudulent"
        elif risk_score >= 0.5:
            return "suspicious"
        else:
            return "legitimate"

    @staticmethod
    def _get_risk_level(risk_score: float) -> str:
        """Get risk level based on score."""
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.6:
            return "medium"
        elif risk_score < 0.8:
            return "high"
        else:
            return "critical"

    @staticmethod
    def _generate_explanation(risk_score: float, is_fraudulent: str) -> str:
        """Generate human-readable explanation."""
        if is_fraudulent == "fraudulent":
            return f"High fraud risk detected. Risk score: {risk_score:.2%}. Transaction should be reviewed immediately."
        elif is_fraudulent == "suspicious":
            return f"Suspicious activity detected. Risk score: {risk_score:.2%}. Additional verification recommended."
        else:
            return f"Transaction appears legitimate. Risk score: {risk_score:.2%}."
