from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

# Base schema
class MaterialBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_url: Optional[str] = None
    file_type: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None
    created_by: Optional[str] = None
    is_active: bool = True

# Schema for creating new material
class MaterialCreate(MaterialBase):
    pass

# Schema for updating material
class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    file_type: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for response
class MaterialResponse(MaterialBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2