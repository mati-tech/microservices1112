from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

# Base schema
class NotificationBase(BaseModel):
    recipient_email: EmailStr
    subject: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    notification_type: NotificationType = NotificationType.EMAIL
    service_source: Optional[str] = None
    event_type: Optional[str] = None

# Schema for sending notification
class NotificationCreate(NotificationBase):
    pass

# Schema for response
class NotificationResponse(NotificationBase):
    id: int
    status: NotificationStatus
    created_at: datetime
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True

# Schema for updating notification
class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None
    error_message: Optional[str] = None

# Schema for retry
class NotificationRetry(BaseModel):
    pass