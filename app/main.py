from fastapi import FastAPI
from models.models import Base
from database.database import engine
from schemas.schema import *
from routes import patient, appointment, billing, department, doctor, inventory, medical_record, staff, user
import uvicorn

app = FastAPI()

app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(billing.router)
app.include_router(department.router)
app.include_router(inventory.router)
app.include_router(doctor.router)
app.include_router(medical_record.router)
app.include_router(staff.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)

    

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1", port=8000)