from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import uuid

class PatientCreate(BaseModel):
    name: str
    date_of_birth: date
    address: str
    city: str
    state: str
    zip_code: str = Field(..., pattern=r'^\d{6}$')
    phone_number: str = Field(..., pattern=r'^\+91\d{10}$', description="Phone number should be 10 digits with country code (+91) optional") 
    email: Optional[EmailStr] = None
    medical_history: str

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone_number: str = Field(..., pattern=r'^\+91\d{10}$', description="Phone number should be 10 digits with country code (+91) optional") 
    email: Optional[EmailStr] = None
    availability_schedule: str

class AppointmentCreate(BaseModel):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID
    date: date
    time: str = Field(..., pattern=r'^(?:[01]\d|2[0-3]):[0-5]\d$', description="Time should be in HH:MM format") 
    status: Optional[str] = "Pending"

    @classmethod
    def validate_date(cls, date: date) -> date: # type: ignore
        if date < date.today():
            raise ValueError('Appointment date must be today or in the future.')
        return date   

class MedicalRecordCreate(BaseModel):
    patient_id: uuid.UUID
    doctor_id: str
    diagnosis: str
    treatment: str
    prescription: str

class BillingCreate(BaseModel):
    patient_id: uuid.UUID
    date: date
    amount: float = Field(gt=0, description="Amount should be positive with 2 decimal places") 
    payment_status: str
    insurance_details: str
    payment_method: str

class InventoryCreate(BaseModel):
    name: str
    quantity: int = Field(gt=0, description="Quantity should be a positive integer") 
    supplier: str
    expiry_date: date
    category : str

    @classmethod
    def validate_date(cls, date: date) -> date: # type: ignore
        if date < date.today():
            raise ValueError('Expire date must be today or in the future.')
        return date

class StaffCreate(BaseModel):
    name: str
    role: str
    phone_number: str = Field(..., pattern=r'^\+91\d{10}$', description="Phone number should be 10 digits with country code (+91) optional") 
    email: Optional[EmailStr] = None
    schedule: str

class DepartmentCreate(BaseModel):
    name: str
    head_of_department_id: str
    contact_information: str

class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8, description="Password should be at least 8 characters long") 
    role: str
