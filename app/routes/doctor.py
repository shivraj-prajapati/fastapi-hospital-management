from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from crud import create_item, get_items, get_item, update_item, delete_item
from database.database import get_db
from models.models import Doctor
from schemas.schema import DoctorCreate
import uuid

router = APIRouter()

@router.post("/doctors/", status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: DoctorCreate, db: Annotated[Session, Depends(get_db)]):
    existing_doctor = db.query(Doctor).filter(Doctor.phone_number == doctor.phone_number).first()
    if existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor with this phone number already exists."
        )
    
    new_doctor = create_item(Doctor, db, **doctor.model_dump())
    
    if not new_doctor:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create doctor."
        )
    
    return new_doctor

@router.get("/doctors/", response_model=List[DoctorCreate], status_code=status.HTTP_200_OK)
async def get_all_doctors(db: Annotated[Session, Depends(get_db)]):
    doctors = get_items(Doctor, db)
    
    if not doctors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No doctors found."
        )
    
    return doctors

@router.get("/doctors/{doctor_id}", response_model=DoctorCreate, status_code=status.HTTP_200_OK)
async def get_doctor(doctor_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    doctor = get_item(Doctor, db, doctor_id)
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found."
        )
    
    return doctor

@router.put("/doctors/{doctor_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_doctor(doctor_id: uuid.UUID, doctor: DoctorCreate, db: Annotated[Session, Depends(get_db)]):
    existing_doctor = get_item(Doctor, db, doctor_id)
    
    if not existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found."
        )
    
    phone_check = db.query(Doctor).filter(Doctor.phone_number == doctor.phone_number, Doctor.id != doctor_id).first()
    if phone_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is already associated with another doctor."
        )
    
    updated_doctor = update_item(Doctor, db, doctor_id, **doctor.model_dump())
    
    if not updated_doctor:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update doctor."
        )
    
    return updated_doctor

@router.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    doctor = get_item(Doctor, db, doctor_id)
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found."
        )
    
    deleted = delete_item(Doctor, db, doctor_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete doctor."
        )
    
    return {"detail": "Doctor deleted successfully"}
