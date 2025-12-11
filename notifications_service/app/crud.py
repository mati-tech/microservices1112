from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from datetime import datetime

# Create notification
def create_notification(db: Session, notification: schemas.NotificationCreate) -> models.Notification:
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

# Get notification by ID
def get_notification(db: Session, notification_id: int) -> Optional[models.Notification]:
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()

# Get all notifications
def get_notifications(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    recipient_email: Optional[str] = None,
    status: Optional[str] = None,
    service_source: Optional[str] = None
) -> List[models.Notification]:
    
    query = db.query(models.Notification)
    
    if recipient_email:
        query = query.filter(models.Notification.recipient_email == recipient_email)
    if status:
        query = query.filter(models.Notification.status == status)
    if service_source:
        query = query.filter(models.Notification.service_source == service_source)
    
    return query.order_by(models.Notification.created_at.desc()).offset(skip).limit(limit).all()

# Update notification status
def update_notification_status(
    db: Session, 
    notification_id: int, 
    status: str,
    error_message: Optional[str] = None
) -> Optional[models.Notification]:
    
    db_notification = get_notification(db, notification_id)
    if not db_notification:
        return None
    
    db_notification.status = status
    db_notification.sent_at = datetime.utcnow() if status == "sent" else None
    if error_message:
        db_notification.error_message = error_message
    
    db.commit()
    db.refresh(db_notification)
    return db_notification

# Get pending notifications
def get_pending_notifications(db: Session, limit: int = 10) -> List[models.Notification]:
    return db.query(models.Notification).filter(
        models.Notification.status == "pending"
    ).order_by(models.Notification.created_at).limit(limit).all()