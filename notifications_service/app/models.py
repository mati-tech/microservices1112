from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from .database import Base

class NotificationType(str, PyEnum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

class NotificationStatus(str, PyEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String(255), nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(SQLEnum(NotificationType), default=NotificationType.EMAIL)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING)
    service_source = Column(String(100))  # e.g., "material_service", "user_service"
    event_type = Column(String(100))      # e.g., "material_created", "user_registered"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, recipient='{self.recipient_email}', status='{self.status}')>"