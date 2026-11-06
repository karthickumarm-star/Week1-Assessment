import csv


# Bonus function
def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# Decorator
def log_call(func):
    def wrapper(*args, **kwargs):
        print("Calling get_details")
        return func(*args, **kwargs)
    return wrapper


# Employee class
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# Manager class
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


# Read CSV file
with open("employees.csv", "r") as file:
    employees = csv.DictReader(file)

    for emp in employees:
        name = emp["name"]
        salary = int(emp["salary"])

        if salary < 50000:
            category = "Low"
        elif salary < 70000:
            category = "Medium"
        else:
            category = "High"

        print(f"{name} - {category} Salary")


# Manager output
manager = Manager("Divya", 75000, 5)
print(manager.get_details())