from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.fraud_prediction import FraudPrediction
from app.db.models.transaction import Transaction
from typing import Optional, List
from datetime import datetime
import random


class FraudPredictionService:
    @staticmethod
    def create_prediction(
        db: Session,
        transaction_id: int,
        risk_score: float,
        confidence_score: float,
        prediction: str,
        explanation: str = None
    ) -> FraudPrediction:
        """Create a fraud prediction."""
        pred = FraudPrediction(
            transaction_id=transaction_id,
            risk_score=risk_score,
            confidence_score=confidence_score,
            prediction=prediction,
            explanation=explanation or ""
        )
        db.add(pred)
        db.commit()
        db.refresh(pred)
        return pred
    
    @staticmethod
    def get_prediction(db: Session, prediction_id: int) -> Optional[FraudPrediction]:
        """Get prediction by ID."""
        return db.query(FraudPrediction).filter(FraudPrediction.id == prediction_id).first()
    
    @staticmethod
    def get_transaction_predictions(
        db: Session,
        transaction_id: int
    ) -> List[FraudPrediction]:
        """Get predictions for a transaction."""
        return db.query(FraudPrediction).filter(
            FraudPrediction.transaction_id == transaction_id
        ).order_by(FraudPrediction.created_at.desc()).all()
    
    @staticmethod
    def list_predictions(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        prediction: Optional[str] = None
    ) -> tuple:
        """List fraud predictions with pagination."""
        query = db.query(FraudPrediction)
        
        if prediction:
            query = query.filter(FraudPrediction.prediction == prediction)
        
        total = query.count()
        predictions = query.order_by(
            FraudPrediction.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return predictions, total
    
    @staticmethod
    def get_prediction_stats(db: Session) -> dict:
        """Get fraud prediction statistics."""
        total_predictions = db.query(func.count(FraudPrediction.id)).scalar() or 0
        fraud_predictions = db.query(func.count(FraudPrediction.id)).filter(
            FraudPrediction.prediction == 'Fraud'
        ).scalar() or 0
        legitimate_predictions = db.query(func.count(FraudPrediction.id)).filter(
            FraudPrediction.prediction == 'Legitimate'
        ).scalar() or 0
        
        avg_confidence = db.query(func.avg(FraudPrediction.confidence_score)).scalar() or 0
        avg_risk = db.query(func.avg(FraudPrediction.risk_score)).scalar() or 0
        
        return {
            'total_predictions': total_predictions,
            'fraud_predictions': fraud_predictions,
            'legitimate_predictions': legitimate_predictions,
            'average_confidence': round(float(avg_confidence), 2),
            'average_risk_score': round(float(avg_risk), 2),
            'fraud_detection_rate': round(
                (fraud_predictions / total_predictions * 100), 2
            ) if total_predictions > 0 else 0
        }
    
    @staticmethod
    def predict_fraud(transaction: Transaction) -> dict:
        """Simple ML-based fraud prediction (placeholder for real model)."""
        # In production, this would use a trained ML model
        risk_score = FraudPredictionService._calculate_risk_score(transaction)
        
        # Determine prediction based on risk score
        if risk_score >= 70:
            prediction = 'Fraud'
            confidence = min(0.95, 0.5 + (risk_score / 200))
        else:
            prediction = 'Legitimate'
            confidence = min(0.95, 0.5 + ((100 - risk_score) / 200))
        
        explanation = FraudPredictionService._generate_explanation(
            transaction, risk_score
        )
        
        return {
            'risk_score': risk_score,
            'confidence_score': round(confidence, 3),
            'prediction': prediction,
            'explanation': explanation
        }
    
    @staticmethod
    def _calculate_risk_score(transaction: Transaction) -> float:
        """Calculate risk score based on transaction features."""
        risk_score = 0
        
        # Amount-based risk
        if transaction.amount > 10000:
            risk_score += 25
        elif transaction.amount > 5000:
            risk_score += 15
        elif transaction.amount > 1000:
            risk_score += 5
        
        # Transaction type risk
        high_risk_types = ['Wire Transfer', 'International', 'Cryptocurrency']
        if transaction.transaction_type in high_risk_types:
            risk_score += 20
        
        # Merchant category risk
        high_risk_merchants = ['Gambling', 'Adult', 'Forex']
        if transaction.merchant_category in high_risk_merchants:
            risk_score += 15
        
        # Time-based risk (late night transactions)
        if transaction.created_at.hour in [0, 1, 2, 3, 4, 5]:
            risk_score += 10
        
        # Add some randomness for demo purposes
        risk_score += random.uniform(-5, 5)
        
        return max(0, min(100, risk_score))
    
    @staticmethod
    def _generate_explanation(transaction: Transaction, risk_score: float) -> str:
        """Generate human-readable explanation for the prediction."""
        factors = []
        
        if transaction.amount > 5000:
            factors.append(f"High transaction amount: ${transaction.amount}")
        
        if transaction.transaction_type in ['Wire Transfer', 'International']:
            factors.append(f"High-risk transaction type: {transaction.transaction_type}")
        
        if transaction.merchant_category:
            factors.append(f"Merchant category: {transaction.merchant_category}")
        
        if risk_score >= 70:
            factors.append("Multiple risk indicators detected")
        
        return "; ".join(factors) if factors else "Standard transaction"
