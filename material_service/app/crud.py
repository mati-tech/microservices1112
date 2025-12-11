from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import models, schemas
from typing import List, Optional

# Create
def create_material(db: Session, material: schemas.MaterialCreate) -> models.Material:
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_material(db: Session, material_id: int) -> Optional[models.Material]:
    return db.query(models.Material).filter(models.Material.id == material_id).first()


def get_materials(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    subject: Optional[str] = None,
    grade_level: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None
) -> List[models.Material]:
    
    query = db.query(models.Material)
    

    if subject:
        query = query.filter(models.Material.subject == subject)
    if grade_level:
        query = query.filter(models.Material.grade_level == grade_level)
    if is_active is not None:
        query = query.filter(models.Material.is_active == is_active)
    if search:
        query = query.filter(
            or_(
                models.Material.title.ilike(f"%{search}%"),
                models.Material.description.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def update_material(
    db: Session, 
    material_id: int, 
    material_update: schemas.MaterialUpdate
) -> Optional[models.Material]:
    
    db_material = get_material(db, material_id)
    if not db_material:
        return None
    update_data = material_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_material, field, value)
    db.commit()
    db.refresh(db_material)
    return db_material

# Delete
def delete_material(db: Session, material_id: int) -> bool:
    db_material = get_material(db, material_id)
    if not db_material:
        return False
    
    db.delete(db_material)
    db.commit()
    return True

# Soft delete (deactivate)
def deactivate_material(db: Session, material_id: int) -> Optional[models.Material]:
    db_material = get_material(db, material_id)
    if not db_material:
        return None
    
    db_material.is_active = False
    db.commit()
    db.refresh(db_material)
    return db_material