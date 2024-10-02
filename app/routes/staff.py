from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from crud import create_item
from database.database import get_db
from models.models import Staff
from schemas.schema import StaffCreate

router = APIRouter()

@router.post("/staff/", status_code=status.HTTP_201_CREATED)
async def create_staff(staff: StaffCreate, db: Annotated[Session, Depends(get_db)]):
    new_staff = Staff(**staff.model_dump())
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    if not new_staff:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create staff.")
    return new_staff

@router.get("/staff", status_code=status.HTTP_200_OK, response_model=List[StaffCreate])
async def get_all_staff(db: Annotated[Session, Depends(get_db)]):
    staff = db.query(Staff).all()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No staff found.")
    return staff


@router.get("/staff/{staff_id}", response_model=StaffCreate, status_code=status.HTTP_200_OK)
async def get_staff(staff_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found.")
    return staff

@router.put("/staff/{staff_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_staff(staff_id: uuid.UUID, staff: StaffCreate, db: Annotated[Session, Depends(get_db)]):
    update_staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not update_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Staff not found.')
    for key, value in staff.model_dump().items():
        setattr(update_staff, key, value)
    db.commit()
    db.refresh(update_staff)
    return update_staff

@router.delete("/staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(staff_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found.")
    db.delete(staff)
    db.commit()
    return {"detail": "Staff deleted successfully"}

