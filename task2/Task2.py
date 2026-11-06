
import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

from openpyxl import Workbook, load_workbook
import fitz

# Logging setup
logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s - %(message)s"
)

BASE_DIR = Path(__file__).parent

# Read CSV file
def read_employees() -> List[dict]:
    file_path = BASE_DIR / "employees.csv"

    with open(file_path, "r", newline="") as file:
        return list(csv.DictReader(file))


# Convert salary
def normalize_salary(value: Union[int, str]) -> int:
    return int(value)


# Write JSON file
def write_json(data: List[dict]) -> None:
    with open(BASE_DIR / "employees.json", "w") as file:
        json.dump(data, file, indent=4)


# Write high earners CSV
def write_high_earners(data: List[dict]) -> int:
    high = [emp for emp in data
            if normalize_salary(emp["salary"]) > 50000]

    with open(BASE_DIR / "high_earners.csv", "w",
              newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "department", "salary"]
        )
        writer.writeheader()
        writer.writerows(high)

    return len(high)


# Create Excel file
def create_excel(data: List[dict]) -> int:
    path = BASE_DIR / "salary.xlsx"

    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Name", "Department", "Salary"])

    for emp in data:
        sheet.append([
            emp["name"],
            emp["department"],
            normalize_salary(emp["salary"])
        ])

    workbook.save(path)

    # Read Excel back
    workbook = load_workbook(path)
    sheet = workbook.active

    return sheet.max_row - 1


# Read JSON file safely
def read_file(path: Union[str, Path]) -> Optional[dict]:
    try:
        with open(path, "r") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

        return None

    except FileNotFoundError:
        logging.error("File not found: %s", Path(path).name)

    except json.JSONDecodeError:
        logging.error("Invalid JSON file: %s", Path(path).name)

    return None


# Find employee
def find_employee(name: str) -> Optional[dict]:
    for emp in employees:
        if emp["name"].lower() == name.lower():
            return emp
    return None


# Main program
employees = read_employees()

write_json(employees)

count = write_high_earners(employees)

print(f"Rows read: {len(employees)} | High earners written: {count}")

rows = create_excel(employees)

print(f"salary.xlsx created and read back: {rows} rows")

# Test missing file
read_file(BASE_DIR / "missing.txt")

# Read PDF page 1
pdf_files = list(BASE_DIR.glob("*.pdf"))

if pdf_files:
    pdf = fitz.open(pdf_files[0])
    text = pdf[0].get_text()
    print("PDF text:", text[:100])
    pdf.close()
else:
    print("PDF not found. Copy a PDF into the project folder.")
