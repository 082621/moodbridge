from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/resources", tags=["Support Resources"])


@router.get("/", response_model=List[schemas.SupportResourceOut])
async def list_resources(
    emotion: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List support resources, optionally filtered by emotion tag or region."""
    query = db.query(models.SupportResource)
    if emotion:
        query = query.filter(models.SupportResource.emotion_tags.contains(emotion))
    if region:
        query = query.filter(models.SupportResource.region == region)
    return query.all()


@router.post("/", response_model=schemas.SupportResourceOut, status_code=status.HTTP_201_CREATED)
async def create_resource(payload: schemas.SupportResourceCreate, db: Session = Depends(get_db)):
    """Create a new support resource."""
    resource = models.SupportResource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@router.put("/{resource_id}", response_model=schemas.SupportResourceOut)
async def update_resource(resource_id: int, payload: schemas.SupportResourceUpdate, db: Session = Depends(get_db)):
    """Update an existing support resource."""
    resource = db.query(models.SupportResource).filter(models.SupportResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    return resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """Delete a support resource."""
    resource = db.query(models.SupportResource).filter(models.SupportResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    db.delete(resource)
    db.commit()
