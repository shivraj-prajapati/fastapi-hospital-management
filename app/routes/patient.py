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
async def create_patients(patient : PatientCreate, db: Annotated[Session, Depends(get_db)]):
    new_patient = Patient(
        name = patient.name,
        date_of_birth = patient.date_of_birth,
        address = patient.address,
        city = patient.city,
        state = patient.state,
        zip_code = patient.zip_code,
        phone_number = patient.phone_number,
        email = patient.email,
        medical_history = patient.medical_history,  
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    if not new_patient:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create patient."
        )
    
    return new_patient

@router.get("/patients", status_code=status.HTTP_200_OK, response_model=List[PatientCreate])
async def get_all_patients(db : Annotated[Session, Depends(get_db)]):
    patient = db.query(Patient).all()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No patients found."
        )
    
    return patient

@router.get("/patients/{patient_id}",response_model=PatientCreate, status_code=status.HTTP_200_OK)
async def get_patient(patient_id: uuid.UUID, db : Annotated[Session, Depends(get_db)]):
    try:
        patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    except SQLAlchemyError as e:
        print(e)
        return None
    return patient

@router.put("/patients/{patient_id}",status_code=status.HTTP_202_ACCEPTED)
async def update_patient(patient_id : uuid.UUID, patient : PatientCreate, db : Annotated[Session, Depends(get_db)]):
    try:
        update_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
        if update_patient is None:
            raise HTTPException(status_code=404, detail='Patient not found.')
        update_patient.name = patient.name,
        update_patient.date_of_birth = patient.date_of_birth,
        update_patient.address = patient.address,
        update_patient.city = patient.city,
        update_patient.state = patient.state,
        update_patient.zip_code = patient.zip_code,
        update_patient.phone_number = patient.phone_number,
        update_patient.email = patient.email,
        update_patient.medical_history = patient.medical_history

        db.add(update_patient)
        db.commit()
        db.refresh(update_patient)
    except SQLAlchemyError as e:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update {Patient.__name__}. Error : {str(e)}"
        )       
        
@router.delete("/patients{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id : uuid.UUID, db : Annotated[Session, Depends(get_db)]):
    try:
        patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
        if not patient:
                return False
        db.delete(patient)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete {Patient.__name__}. Error: {str(e)}"
        )