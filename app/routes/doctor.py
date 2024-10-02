from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from crud import create_item, get_items, get_item, update_item, delete_item
from database.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from models.models import Doctor
from schemas.schema import DoctorCreate
import uuid

router = APIRouter()

@router.post("/doctors/", status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: DoctorCreate, db: Annotated[Session, Depends(get_db)]):
    new_doctor = Doctor(**doctor.model_dump())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    if not new_doctor:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create doctor")
    return new_doctor

@router.get("/doctors/", response_model=List[DoctorCreate], status_code=status.HTTP_200_OK)
async def get_all_doctors(db: Annotated[Session, Depends(get_db)]):
    doctors = db.query(Doctor).all()
    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No doctors found.")
    return doctors

@router.get("/doctors/{doctor_id}", response_model=DoctorCreate, status_code=status.HTTP_200_OK)
async def get_doctor(doctor_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    try:
        doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    except SQLAlchemyError as e:
        print(e)
        return None
    return doctor

@router.put("/doctors/{doctor_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_doctor(doctor_id: uuid.UUID, doctor: DoctorCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        update_doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
        if update_doctor is None:
            raise HTTPException(status_code=404, detail="Doctor not found.")
        for key, value in doctor.model_dump().items():
            setattr(update_doctor, key, value)
        db.commit()
        db.refresh(update_doctor)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update {Doctor.__name__}. Error : {str(e)}")
    return {"detail": "Doctor updated successfully", "doctor": update_doctor}

@router.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    doctor = get_item(Doctor, db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
    deleted = delete_item(Doctor, db, doctor_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete doctor.")
    return {"detail": "Doctor deleted successfully"}
