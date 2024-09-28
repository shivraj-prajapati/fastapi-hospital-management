import uuid
from database.database import Base
from sqlalchemy import (Column, Date, Float, String, Integer, ForeignKey, Text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = 'patients'

    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    medical_history = Column(Text)
    

class Doctor(Base):
    __tablename__ = 'doctors'
    
    doctor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    availability_schedule = Column(Text, nullable=True)
    

class Appointment(Base):
    __tablename__ = 'appointments'
    
    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.patient_id'))
    doctor_id = Column(UUID(as_uuid=True), ForeignKey('doctors.doctor_id'))
    date = Column(Date, nullable=False)
    time = Column(String, nullable=False)
    status = Column(String, nullable=False)
    
    patient = relationship('Patient')
    doctor = relationship('Doctor')

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
     
    record_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.patient_id'))
    doctor_id = Column(UUID(as_uuid=True), ForeignKey('doctors.doctor_id'))
    diagnosis = Column(Text, nullable=False)
    treatment = Column(Text, nullable=False)
    prescription = Column(Text, nullable=True)
    
    patient = relationship('Patient')
    doctor = relationship('Doctor')

class Billing(Base):
    __tablename__ = 'billing'
    
    bill_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.patient_id'))
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String, nullable=False)
    insurance_details = Column(String, nullable=True)
    payment_method = Column(String, nullable=False) 

    patient = relationship("Patient")   
    
class Inventory(Base):
    __tablename__ = 'inventory'

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    supplier = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=False)
    category = Column(String, nullable=False)    
    
class Staff(Base):
    __tablename__ = 'staff'
    
    staff_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    schedule = Column(Text, nullable=True)


class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    head_of_department_id = Column(UUID(as_uuid=True), ForeignKey('staff.staff_id'))
    contact_information = Column(String, nullable=False)
    
    head_of_department = relationship('Staff')
    
class User(Base):
    __tablename__ = 'users'
        
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    