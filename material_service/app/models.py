from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    content_url = Column(String(500))  # URL to PDF/video/other content
    file_type = Column(String(50))     # pdf, video, doc, etc.
    subject = Column(String(100), index=True)
    grade_level = Column(String(50))   # e.g., "Grade 10", "University"
    created_by = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Material(id={self.id}, title='{self.title}')>"