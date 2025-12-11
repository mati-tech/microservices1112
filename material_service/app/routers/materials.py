from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/materials", tags=["materials"])

# Create material
@router.post("/", response_model=schemas.MaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(
    material: schemas.MaterialCreate,
    db: Session = Depends(get_db)
):
    return crud.create_material(db=db, material=material)

# Get all materials with filters
@router.get("/", response_model=List[schemas.MaterialResponse])
def read_materials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    subject: Optional[str] = None,
    grade_level: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    materials = crud.get_materials(
        db=db,
        skip=skip,
        limit=limit,
        subject=subject,
        grade_level=grade_level,
        is_active=is_active,
        search=search
    )
    return materials

# Get material by ID
@router.get("/{material_id}", response_model=schemas.MaterialResponse)
def read_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.get_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with ID {material_id} not found"
        )
    return db_material

# Update material
@router.put("/{material_id}", response_model=schemas.MaterialResponse)
def update_material(
    material_id: int,
    material_update: schemas.MaterialUpdate,
    db: Session = Depends(get_db)
):
    db_material = crud.update_material(db, material_id=material_id, material_update=material_update)
    if db_material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with ID {material_id} not found"
        )
    return db_material

# Delete material (hard delete)
@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    success = crud.delete_material(db, material_id=material_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with ID {material_id} not found"
        )
    return None

# Deactivate material (soft delete)
@router.patch("/{material_id}/deactivate", response_model=schemas.MaterialResponse)
def deactivate_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.deactivate_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with ID {material_id} not found"
        )
    return db_material


# # NEW: Simple search by name/title
# @router.get("/search/", response_model=List[schemas.MaterialResponse])
# def search_materials_by_name(
#     name: str = Query(..., description="Search term for material name/title"),
#     db: Session = Depends(get_db)
# ):
#     """Search materials by name/title (case-insensitive partial match)"""
#     # Use SQLAlchemy's ilike for case-insensitive search
#     from sqlalchemy import or_
    
#     materials = db.query(models.Material).filter(
#         models.Material.title.ilike(f"%{name}%")
#     ).all()
    
#     return materials