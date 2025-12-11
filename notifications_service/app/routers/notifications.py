from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

from .. import crud, schemas
from ..database import get_db
from ..email.sender import email_sender
from ..email import templates as email_templates

router = APIRouter(prefix="/notifications", tags=["notifications"])

# Send notification (main endpoint)
@router.post("/send", response_model=schemas.NotificationResponse, status_code=status.HTTP_201_CREATED)
async def send_notification(
    notification: schemas.NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send a notification (email).
    
    The email will be sent in the background.
    Returns immediately with notification record.
    """
    # Create notification record
    db_notification = crud.create_notification(db=db, notification=notification)
    
    # Schedule email sending in background
    background_tasks.add_task(
        send_email_background,
        db_notification.id,
        db_notification.recipient_email,
        db_notification.subject,
        db_notification.message,
        db
    )
    
    return db_notification

# Send notification immediately (synchronous)
@router.post("/send-now", response_model=schemas.NotificationResponse)
async def send_notification_now(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db)
):
    """
    Send a notification immediately and wait for result.
    
    Use this for testing or when you need to know if email was sent.
    """
    # Create notification record
    db_notification = crud.create_notification(db=db, notification=notification)
    
    # Send email immediately
    success = email_sender.send_email(
        to_email=db_notification.recipient_email,
        subject=db_notification.subject,
        message=db_notification.message,
        html_message=email_templates.render_simple_notification_template(
            db_notification.subject,
            db_notification.message
        )
    )
    
    # Update status
    if success:
        crud.update_notification_status(db, db_notification.id, "sent")
    else:
        crud.update_notification_status(db, db_notification.id, "failed", "Failed to send email")
    
    # Refresh and return
    db.refresh(db_notification)
    return db_notification

# Get all notifications
@router.get("/", response_model=List[schemas.NotificationResponse])
def read_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    recipient_email: Optional[str] = None,
    status: Optional[str] = None,
    service_source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    notifications = crud.get_notifications(
        db=db,
        skip=skip,
        limit=limit,
        recipient_email=recipient_email,
        status=status,
        service_source=service_source
    )
    return notifications

# Get notification by ID
@router.get("/{notification_id}", response_model=schemas.NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found"
        )
    return db_notification

# Retry failed notification
@router.post("/{notification_id}/retry", response_model=schemas.NotificationResponse)
async def retry_notification(
    notification_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found"
        )
    
    if db_notification.status != "failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only retry failed notifications"
        )
    
    # Reset to pending
    db_notification.status = "pending"
    db_notification.error_message = None
    db.commit()
    db.refresh(db_notification)
    
    # Retry in background
    background_tasks.add_task(
        send_email_background,
        db_notification.id,
        db_notification.recipient_email,
        db_notification.subject,
        db_notification.message,
        db
    )
    
    return db_notification

# Send test email
@router.post("/test-email", status_code=status.HTTP_200_OK)
async def send_test_email(
    email: str = Query(..., description="Email address to send test to"),
    db: Session = Depends(get_db)
):
    """Send a test email to verify SMTP configuration"""
    test_subject = "Test Email from Notification Service"
    test_message = "This is a test email to verify the notification service is working correctly."
    
    success = email_sender.send_email(
        to_email=email,
        subject=test_subject,
        message=test_message,
        html_message=email_templates.render_simple_notification_template(test_subject, test_message)
    )
    
    if success:
        return {"message": f"Test email sent successfully to {email}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test email. Check SMTP configuration."
        )

# Background task function
async def send_email_background(notification_id: int, recipient_email: str, subject: str, message: str, db: Session):
    """Background task to send email and update status"""
    try:
        # Send email
        success = email_sender.send_email(
            to_email=recipient_email,
            subject=subject,
            message=message,
            html_message=email_templates.render_simple_notification_template(subject, message)
        )
        
        # Update status in database
        if success:
            crud.update_notification_status(db, notification_id, "sent")
        else:
            crud.update_notification_status(db, notification_id, "failed", "Failed to send email")
            
    except Exception as e:
        # Log error and update status
        crud.update_notification_status(db, notification_id, "failed", str(e))