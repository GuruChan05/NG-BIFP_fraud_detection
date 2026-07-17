from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.fraud_prediction import FraudPredictionResponse, FraudPredictionCreate
from app.services.fraud_prediction import FraudPredictionService
from app.db.models.user import User
from app.db.models.transaction import Transaction
from app.api.deps import get_current_active_user
from typing import List

router = APIRouter()


@router.get("/stats")
async def get_prediction_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get fraud prediction statistics."""
    return FraudPredictionService.get_prediction_stats(db)


@router.get("/", response_model=List[FraudPredictionResponse])
async def list_predictions(
    skip: int = 0,
    limit: int = 20,
    prediction: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List fraud predictions with pagination."""
    predictions, total = FraudPredictionService.list_predictions(
        db, skip, limit, prediction
    )
    return predictions


@router.get("/{prediction_id}", response_model=FraudPredictionResponse)
async def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get prediction by ID."""
    prediction = FraudPredictionService.get_prediction(db, prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction


@router.get("/transaction/{transaction_id}")
async def get_transaction_predictions(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get predictions for a specific transaction."""
    # Verify transaction exists
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    predictions = FraudPredictionService.get_transaction_predictions(
        db, transaction_id
    )
    return predictions


@router.post("/predict")
async def predict_fraud(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Run fraud prediction on a transaction."""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Generate prediction
    prediction_data = FraudPredictionService.predict_fraud(transaction)
    
    # Store prediction
    prediction = FraudPredictionService.create_prediction(
        db=db,
        transaction_id=transaction_id,
        risk_score=prediction_data['risk_score'],
        confidence_score=prediction_data['confidence_score'],
        prediction=prediction_data['prediction'],
        explanation=prediction_data['explanation']
    )
    
    # Update transaction with prediction
    transaction.risk_score = prediction_data['risk_score']
    transaction.is_fraudulent = prediction_data['prediction']
    db.commit()
    
    return prediction_data
