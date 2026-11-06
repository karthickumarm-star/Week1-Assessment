 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Employee(BaseModel):
    name: str = Field(..., min_length=1)
    salary: float

employees = []

# Health Check
@app.get("/health")
def health():
    return {"status": "ok"}


# Get All Employees
@app.get("/employees")
def get_employees():
    return employees


# Add Employee
@app.post("/employees")
def add_employee(employee: Employee):

    if employee.salary <= 0:
        raise HTTPException(
            status_code=422,
            detail="Invalid salary"
        )

    employees.append(employee.model_dump())

    return employee


# Get Employee By Name
@app.get("/employees/{name}")
def get_employee(name: str):

    for employee in employees:

        if isinstance(employee, dict):
            employee_name = employee["name"]
        else:
            employee_name = employee.name

        if employee_name.lower() == name.lower():
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )
