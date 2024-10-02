from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database.database import get_db
from models.models import Department
from schemas.schema import DepartmentCreate

router = APIRouter()

@router.post("/departments/",status_code=status.HTTP_201_CREATED)
async def create_department(department: DepartmentCreate, db: Annotated[Session, Depends(get_db)]):
    new_department = Department(**department.model_dump())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    if not new_department:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create department.")
    return new_department

@router.get("/departments", status_code=status.HTTP_200_OK)
async def get_all_departments(db: Annotated[Session, Depends(get_db)]):
    departments = db.query(Department).all()
    if not departments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No departments found.")
    return departments

@router.get("/departments/{department_id}", status_code=status.HTTP_200_OK)
async def get_department(department_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    department = db.query(Department).filter(Department.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found.")
    return department

@router.put("/departments/{department_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_department(department_id: uuid.UUID, department: DepartmentCreate, db: Annotated[Session, Depends(get_db)]):
    update_department = db.query(Department).filter(Department.department_id == department_id).first()
    if not update_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not found.')
    for key, value in department.model_dump().items():
        setattr(update_department, key, value)
    db.commit()
    db.refresh(update_department)
    return update_department

@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    department = db.query(Department).filter(Department.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found.")
    db.delete(department)
    db.commit()
    return {"detail": "Department deleted successfully"}
