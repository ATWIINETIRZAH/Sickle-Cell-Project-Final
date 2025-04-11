
# from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from database import Base

# class Patient(Base):
#     __tablename__ = "patients"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     contact = Column(String, nullable=False)
#     next_appointment = Column(DateTime, default=datetime.utcnow)
    
#     cbc_reports = relationship("CBCReport", back_populates="patient")

# class CBCReport(Base):
#     __tablename__ = "cbc_reports"

#     id = Column(Integer, primary_key=True, index=True)
#     patient_id = Column(Integer, ForeignKey("patients.id"))
#     rbc = Column(Float)
#     hgb = Column(Float)
#     wbc = Column(Float)
#     plt = Column(Float)
#     neutp = Column(Float)
#     uploaded_at = Column(DateTime, default=datetime.utcnow)
    
#     patient = relationship("Patient", back_populates="cbc_reports")


from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    next_appointment = Column(String, nullable=False)  # Changed to String for manual entry
    
    cbc_reports = relationship("CBCReport", back_populates="patient")

class CBCReport(Base):
    __tablename__ = "cbc_reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    rbc = Column(Float)
    hgb = Column(Float)
    wbc = Column(Float)
    plt = Column(Float)
    neutp = Column(Float)
    uploaded_at = Column(String, nullable=False)  # Changed to String for manual entry
    
    patient = relationship("Patient", back_populates="cbc_reports")
