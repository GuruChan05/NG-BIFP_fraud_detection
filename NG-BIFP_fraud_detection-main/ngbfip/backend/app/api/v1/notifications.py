"""Notification API endpoints with full CRUD operations."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.db.models.user import User
from app.services.notification_service import NotificationService
from app.schemas.notification import (
    NotificationResponse,
    NotificationCreate,
    NotificationUpdate,
    NotificationListResponse,
    BulkMarkAsReadRequest,
    NotificationStatsResponse,
)

router = APIRouter()


@router.get("/", response_model=NotificationListResponse)
async def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    unread_only: bool = Query(False),
):
    """
    List all notifications for the current user.
    
    Query parameters:
    - skip: Number of notifications to skip
    - limit: Maximum number of notifications to return (max 100)
    - unread_only: If true, return only unread notifications
    """
    try:
        notifications, total = NotificationService.list_notifications(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            unread_only=unread_only,
        )
        unread_count = NotificationService.get_unread_count(db, current_user.id)
        
        return NotificationListResponse(
            total=total,
            unread_count=unread_count,
            data=[NotificationResponse.from_orm(n) for n in notifications],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching notifications: {str(e)}",
        )


@router.get("/stats", response_model=NotificationStatsResponse)
async def get_notification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get notification statistics for the current user."""
    try:
        stats = NotificationService.get_notification_stats(db, current_user.id)
        return NotificationStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching notification stats: {str(e)}",
        )


@router.get("/unread-count")
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get count of unread notifications."""
    try:
        count = NotificationService.get_unread_count(db, current_user.id)
        return {"unread_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching unread count: {str(e)}",
        )


@router.post("/", response_model=NotificationResponse)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new notification.
    Admin only - notifications should typically be created by system events.
    """
    try:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can create notifications",
            )
        
        db_notification = NotificationService.create_notification(
            db=db,
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            notification_type=notification.notification_type,
            related_transaction_id=notification.related_transaction_id,
            related_alert_id=notification.related_alert_id,
        )
        return NotificationResponse.from_orm(db_notification)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating notification: {str(e)}",
        )


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific notification by ID."""
    try:
        notification = NotificationService.get_notification_by_id(db, notification_id)
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        
        # Check ownership
        if notification.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this notification",
            )
        
        return NotificationResponse.from_orm(notification)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching notification: {str(e)}",
        )


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a notification (typically just marking as read)."""
    try:
        notification = NotificationService.get_notification_by_id(db, notification_id)
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        
        # Check ownership
        if notification.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this notification",
            )
        
        # Update fields
        if notification_update.is_read is not None:
            notification.is_read = notification_update.is_read
        if notification_update.title is not None:
            notification.title = notification_update.title
        if notification_update.message is not None:
            notification.message = notification_update.message
        
        db.commit()
        db.refresh(notification)
        
        return NotificationResponse.from_orm(notification)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating notification: {str(e)}",
        )


@router.post("/{notification_id}/mark-as-read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Mark a single notification as read."""
    try:
        notification = NotificationService.mark_as_read(db, notification_id, current_user.id)
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found or not authorized",
            )
        
        return NotificationResponse.from_orm(notification)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error marking notification as read: {str(e)}",
        )


@router.post("/mark-all-as-read")
async def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Mark all notifications as read."""
    try:
        count = NotificationService.mark_all_as_read(db, current_user.id)
        return {"message": f"Marked {count} notifications as read", "count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error marking notifications as read: {str(e)}",
        )


@router.post("/bulk-mark-as-read")
async def bulk_mark_as_read(
    request: BulkMarkAsReadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Mark multiple notifications as read."""
    try:
        count = NotificationService.bulk_mark_as_read(db, request.notification_ids, current_user.id)
        return {"message": f"Marked {count} notifications as read", "count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error marking notifications as read: {str(e)}",
        )


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a notification."""
    try:
        success = NotificationService.delete_notification(db, notification_id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found or not authorized",
            )
        
        return {"message": "Notification deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting notification: {str(e)}",
        )


@router.post("/bulk-delete")
async def bulk_delete_notifications(
    request: BulkMarkAsReadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete multiple notifications."""
    try:
        count = NotificationService.delete_multiple(db, request.notification_ids, current_user.id)
        return {"message": f"Deleted {count} notifications", "count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting notifications: {str(e)}",
        )


@router.get("/history/all", response_model=NotificationListResponse)
async def get_notification_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    days: int = Query(30, ge=1, le=365),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """Get notification history for the current user."""
    try:
        notifications, total = NotificationService.get_notification_history(
            db=db,
            user_id=current_user.id,
            days=days,
            skip=skip,
            limit=limit,
        )
        unread_count = NotificationService.get_unread_count(db, current_user.id)
        
        return NotificationListResponse(
            total=total,
            unread_count=unread_count,
            data=[NotificationResponse.from_orm(n) for n in notifications],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching notification history: {str(e)}",
        )


@router.get("/type/{notification_type}", response_model=NotificationListResponse)
async def get_notifications_by_type(
    notification_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Get notifications filtered by type."""
    try:
        notifications, total = NotificationService.get_notifications_by_type(
            db=db,
            user_id=current_user.id,
            notification_type=notification_type,
            skip=skip,
            limit=limit,
        )
        unread_count = NotificationService.get_unread_count(db, current_user.id)
        
        return NotificationListResponse(
            total=total,
            unread_count=unread_count,
            data=[NotificationResponse.from_orm(n) for n in notifications],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching notifications by type: {str(e)}",
        )


@router.post("/clear-old")
async def clear_old_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    days: int = Query(30, ge=1, le=365),
):
    """Clear notifications older than specified days."""
    try:
        count = NotificationService.clear_old_notifications(db, current_user.id, days)
        return {"message": f"Cleared {count} old notifications", "count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing old notifications: {str(e)}",
        )
