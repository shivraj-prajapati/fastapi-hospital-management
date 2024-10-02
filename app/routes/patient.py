from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from models.models import Patient
from schemas.schema import PatientCreate

router = APIRouter()

@router.post("/patients/", status_code=status.HTTP_201_CREATED)
async def create_patients(patient: PatientCreate, db: Annotated[Session, Depends(get_db)]):
    new_patient = Patient(**patient.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    if not new_patient:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create patient.")
    return new_patient

@router.get("/patients", status_code=status.HTTP_200_OK, response_model=List[PatientCreate])
async def get_all_patients(db: Annotated[Session, Depends(get_db)]):
    patients = db.query(Patient).all()
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No patients found.")
    return patients

@router.get("/patients/{patient_id}", response_model=PatientCreate, status_code=status.HTTP_200_OK)
async def get_patient(patient_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return patient

@router.put("/patients/{patient_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_patient(patient_id: uuid.UUID, patient: PatientCreate, db: Annotated[Session, Depends(get_db)]):
    update_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not update_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Patient not found.')
    for key, value in patient.model_dump().items():
        setattr(update_patient, key, value)
    db.commit()
    db.refresh(update_patient)
    return update_patient

@router.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted successfully"}
