from dataclasses import dataclass, field
from typing import List, Optional
import uuid
from datetime import datetime

@dataclass
class Patient:
    id: str
    name: str
    age: int
    disease: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%d %b %Y"))

@dataclass
class Bill:
    id: str
    patient_id: str
    patient_name: str
    amount: float
    status: str  # "paid" | "pending" | "overdue"
    description: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%d %b %Y"))


class PatientDB:
    _patients: List[Patient] = [
        Patient("p1", "Arjun Mehta", 54, "Diabetes"),
        Patient("p2", "Priya Sharma", 38, "Hypertension"),
        Patient("p3", "Rohan Verma", 67, "Heart Failure"),
        Patient("p4", "Ananya Iyer", 29, "Asthma"),
        Patient("p5", "Vikram Nair", 45, "Tuberculosis"),
    ]

    @classmethod
    def all(cls) -> List[Patient]:
        return cls._patients

    @classmethod
    def get(cls, patient_id: str) -> Optional[Patient]:
        return next((p for p in cls._patients if p.id == patient_id), None)

    @classmethod
    def add(cls, name: str, age: int, disease: str) -> Patient:
        p = Patient(id=str(uuid.uuid4())[:8], name=name, age=age, disease=disease)
        cls._patients.append(p)
        return p

    @classmethod
    def delete(cls, patient_id: str):
        cls._patients = [p for p in cls._patients if p.id != patient_id]


class BillingDB:
    _bills: List[Bill] = [
        Bill("b1", "p1", "Arjun Mehta", 3500.00, "paid", "Consultation + Lab Tests"),
        Bill("b2", "p2", "Priya Sharma", 1200.00, "pending", "Cardiology Consultation"),
        Bill("b3", "p3", "Rohan Verma", 8750.00, "overdue", "ICU Charges – Day 1"),
        Bill("b4", "p4", "Ananya Iyer", 950.00, "paid", "Pulmonology Review"),
        Bill("b5", "p5", "Vikram Nair", 5200.00, "pending", "DOTS Therapy Initiation"),
    ]

    @classmethod
    def all(cls) -> List[Bill]:
        return cls._bills

    @classmethod
    def add(cls, patient_id: str, patient_name: str, amount: float, status: str, description: str) -> Bill:
        b = Bill(
            id=str(uuid.uuid4())[:8],
            patient_id=patient_id,
            patient_name=patient_name,
            amount=amount,
            status=status,
            description=description,
        )
        cls._bills.append(b)
        return b

    @classmethod
    def delete(cls, bill_id: str):
        cls._bills = [b for b in cls._bills if b.id != bill_id]

    @classmethod
    def update_status(cls, bill_id: str, new_status: str):
        for b in cls._bills:
            if b.id == bill_id:
                b.status = new_status
                break