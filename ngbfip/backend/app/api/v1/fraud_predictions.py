"""Fraud prediction API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.db.models.user import User
from app.services.fraud_prediction import FraudPredictionService
from app.schemas.fraud_prediction import (
    FraudPredictionRequest,
    FraudPredictionResponse,
    PredictionHistoryResponse,
    PredictionHistoryEntry,
    BulkPredictionRequest,
    BulkPredictionResponse,
)
import json
from datetime import datetime

router = APIRouter()
prediction_service = FraudPredictionService()


@router.post("/predict", response_model=FraudPredictionResponse)
async def predict_fraud(
    request: FraudPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Predict fraud risk for a transaction.
    
    Returns risk score, confidence score, and explanation.
    """
    try:
        prediction = prediction_service.predict(db, request)

        return FraudPredictionResponse(
            transaction_id=prediction.transaction_id,
            risk_score=prediction.risk_score,
            confidence_score=prediction.confidence_score,
            is_fraudulent=prediction.is_fraudulent,
            risk_level=prediction.risk_level,
            explanation=prediction.explanation,
            contributing_factors=json.loads(prediction.contributing_factors),
            recommendations=json.loads(prediction.recommendations),
            prediction_timestamp=prediction.created_at,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error making prediction: {str(e)}",
        )


@router.post("/predict/bulk", response_model=BulkPredictionResponse)
async def predict_fraud_bulk(
    request: BulkPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Make fraud predictions for multiple transactions.
    """
    try:
        predictions = []
        successful = 0
        failed = 0

        for transaction_request in request.transactions:
            try:
                prediction = prediction_service.predict(db, transaction_request)
                predictions.append(
                    FraudPredictionResponse(
                        transaction_id=prediction.transaction_id,
                        risk_score=prediction.risk_score,
                        confidence_score=prediction.confidence_score,
                        is_fraudulent=prediction.is_fraudulent,
                        risk_level=prediction.risk_level,
                        explanation=prediction.explanation,
                        contributing_factors=json.loads(prediction.contributing_factors),
                        recommendations=json.loads(prediction.recommendations),
                        prediction_timestamp=prediction.created_at,
                    )
                )
                successful += 1
            except Exception:
                failed += 1

        return BulkPredictionResponse(
            total=len(request.transactions),
            successful=successful,
            failed=failed,
            predictions=predictions,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing bulk predictions: {str(e)}",
        )


@router.get("/history", response_model=PredictionHistoryResponse)
async def get_prediction_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get prediction history for the current user.
    """
    try:
        predictions, total = prediction_service.get_user_prediction_history(
            db, current_user.id, page=page, page_size=page_size
        )

        total_pages = (total + page_size - 1) // page_size

        return PredictionHistoryResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            data=[
                PredictionHistoryEntry(
                    id=p.id,
                    user_id=p.user_id,
                    transaction_id=p.transaction_id,
                    risk_score=p.risk_score,
                    confidence_score=p.confidence_score,
                    is_fraudulent=p.is_fraudulent,
                    risk_level=p.risk_level,
                    explanation=p.explanation,
                    created_at=p.created_at,
                )
                for p in predictions
            ],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching prediction history: {str(e)}",
        )


@router.get("/stats")
async def get_prediction_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get fraud prediction statistics.
    """
    try:
        stats = prediction_service.get_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}",
        )


@router.get("/model/info")
async def get_model_info(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get information about the fraud detection model.
    """
    try:
        return prediction_service.model.get_model_info()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching model info: {str(e)}",
        )
