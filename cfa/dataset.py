import os
import csv
import json
import random
import datetime
import uuid
import numpy as np
from pathlib import Path
from faker import Faker

# Initialize faker for generating realistic data
fake = Faker()

# Get project root path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

# Configuration
NUM_CONTRACTS = 500  # Number of contracts
NUM_VENDORS = 200  # Number of vendors
NUM_PROJECTS = 50  # Number of projects
NUM_TRANSACTIONS = 50000  # Number of financial transactions
NUM_MODIFICATIONS = 2000  # Number of contract modifications
NUM_DELIVERABLES = 5000  # Number of contract deliverables

# File paths
CONTRACTS_FILE = os.path.join(DATA_DIR, "contracts.csv")
VENDORS_FILE = os.path.join(DATA_DIR, "vendors.json")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")
MODIFICATIONS_FILE = os.path.join(DATA_DIR, "contract_modifications.csv")
DELIVERABLES_FILE = os.path.join(DATA_DIR, "deliverables.csv")
PERSONNEL_FILE = os.path.join(DATA_DIR, "personnel.csv")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Constants for data generation
CONTRACT_TYPES = [
    "Firm-Fixed-Price",
    "Cost-Plus-Fixed-Fee",
    "Time-and-Materials",
    "Indefinite-Delivery",
    "Cost-Plus-Incentive-Fee",
    "Cost-Plus-Award-Fee",
]

PROJECT_TYPES = [
    "Research",
    "Development",
    "Testing",
    "Production",
    "Maintenance",
    "IT Services",
    "Consulting",
    "Training",
    "Construction",
    "Logistics",
]

TRANSACTION_TYPES = ["Labor", "Material", "Travel", "Subcontract", "ODC", "Fee"]

CONTRACT_STATUS = ["Active", "Completed", "Terminated", "On Hold", "In Negotiation"]

DEPARTMENTS = ["Navy", "Army", "Air Force", "Marines", "Coast Guard", "DLA", "DARPA", "NSA", "DIA"]

PERSONNEL_ROLES = [
    "Project Manager",
    "Financial Analyst",
    "Contract Specialist",
    "Program Manager",
    "Technical Lead",
    "Engineer",
    "Quality Assurance",
    "Subject Matter Expert",
]

MODIFICATION_TYPES = [
    "Administrative",
    "Funding",
    "Schedule",
    "Scope Change",
    "Extension",
    "Termination",
]

DELIVERABLE_TYPES = [
    "Report",
    "Software",
    "Hardware",
    "Documentation",
    "Prototype",
    "Training",
    "Data",
]

# Generate IDs first
contract_ids = [f"CTR-{i:06d}" for i in range(1, NUM_CONTRACTS + 1)]
vendor_ids = [f"VEN-{i:04d}" for i in range(1, NUM_VENDORS + 1)]
project_ids = [f"PRJ-{i:04d}" for i in range(1, NUM_PROJECTS + 1)]
personnel_ids = [f"PER-{i:05d}" for i in range(1, 1000 + 1)]  # 1000 personnel

# Mappings for relationships
contract_to_vendor = {}
contract_to_project = {}
contract_values = {}


def generate_contracts():
    """Generate contract data"""
    print("Generating contract data...")

    with open(CONTRACTS_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "contract_id",
                "contract_number",
                "vendor_id",
                "project_id",
                "contract_type",
                "start_date",
                "end_date",
                "original_value",
                "current_value",
                "status",
                "department",
                "description",
                "contracting_officer",
            ]
        )

        start_years = list(range(2018, 2025))

        for contract_id in contract_ids:
            contract_number = f"N00{random.randint(10000, 99999)}-{random.randint(10, 99)}-D-{random.randint(1000, 9999)}"
            vendor_id = random.choice(vendor_ids)
            project_id = random.choice(project_ids)
            contract_type = random.choice(CONTRACT_TYPES)

            # Store relationships for later use
            contract_to_vendor[contract_id] = vendor_id
            contract_to_project[contract_id] = project_id

            # Generate dates with majority being recent but some older contracts
            start_year = random.choices(start_years, weights=[1, 2, 3, 5, 7, 10, 15], k=1)[0]
            start_date_obj = datetime.date(start_year, 1, 1)
            end_date_obj = datetime.date(start_year, 12, 31)
            start_date = fake.date_between(start_date=start_date_obj, end_date=end_date_obj)

            # Contract duration between 1 and 5 years, weighted toward shorter
            duration_years = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5], k=1)[0]
            end_date = start_date + datetime.timedelta(days=365 * duration_years)

            # Generate contract values, typically between $100K and $50M
            original_value = round(random.uniform(100000, 50000000), 2)

            # Current value might be different from original due to modifications
            # Weighted to have some overruns, some underruns, and many on target
            modifier = random.choices(
                [0.8, 0.9, 1.0, 1.1, 1.2, 1.5], weights=[5, 15, 50, 20, 8, 2], k=1
            )[0]
            current_value = round(original_value * modifier, 2)

            # Store for later reference
            contract_values[contract_id] = current_value

            # Status weighted toward active
            status = random.choices(CONTRACT_STATUS, weights=[60, 25, 5, 5, 5], k=1)[0]
            department = random.choice(DEPARTMENTS)
            description = fake.bs()  # Business jargon for description
            contracting_officer = personnel_ids[random.randint(0, len(personnel_ids) - 1)]

            writer.writerow(
                [
                    contract_id,
                    contract_number,
                    vendor_id,
                    project_id,
                    contract_type,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    f"{original_value:.2f}",
                    f"{current_value:.2f}",
                    status,
                    department,
                    description,
                    contracting_officer,
                ]
            )

    print(f"✅ Generated {NUM_CONTRACTS} contracts")


def generate_vendors():
    """Generate vendor data"""
    print("Generating vendor data...")

    vendors = []
    for vendor_id in vendor_ids:
        vendor_size = random.choice(["Small", "Medium", "Large", "Very Large"])

        # Generate some realistic procurement categories
        categories = random.sample(
            [
                "IT Services",
                "Hardware",
                "Software",
                "Engineering",
                "R&D",
                "Professional Services",
                "Manufacturing",
                "Logistics",
                "Consulting",
                "Training",
                "Facilities",
                "Security",
                "Telecommunications",
            ],
            k=random.randint(1, 5),
        )

        # Financial metrics
        annual_revenue = round(random.uniform(1000000, 5000000000), 2)

        # Contract history - some metrics about past performance
        past_performance = {
            "on_time_delivery_rate": round(random.uniform(0.7, 1.0), 2),
            "quality_rating": round(random.uniform(3.0, 5.0), 1),
            "cost_variance": round(random.uniform(-0.2, 0.3), 2),  # negative is under budget
            "contracts_completed": random.randint(5, 200),
            "avg_contract_value": round(random.uniform(100000, 10000000), 2),
        }

        vendor = {
            "vendor_id": vendor_id,
            "name": fake.company(),
            "duns_number": f"{random.randint(100000000, 999999999)}",
            "cage_code": f"{random.randint(10000, 99999)}",
            "address": fake.address().replace("\n", ", "),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "phone": fake.phone_number(),
            "email": fake.company_email(),
            "website": fake.url(),
            "size": vendor_size,
            "categories": categories,
            "socioeconomic": random.sample(
                ["8(a)", "SDVOSB", "WOSB", "HUBZone", "SB", "LB"], k=random.randint(0, 3)
            ),
            "annual_revenue": annual_revenue,
            "year_established": random.randint(1950, 2020),
            "past_performance": past_performance,
            "active_contracts": random.randint(1, 30),
            "point_of_contact": {
                "name": fake.name(),
                "title": fake.job(),
                "phone": fake.phone_number(),
                "email": fake.email(),
            },
        }
        vendors.append(vendor)

    with open(VENDORS_FILE, "w") as f:
        json.dump(vendors, f, indent=2)

    print(f"✅ Generated {NUM_VENDORS} vendors")


def generate_projects():
    """Generate project data"""
    print("Generating project data...")

    with open(PROJECTS_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "project_id",
                "name",
                "type",
                "description",
                "start_date",
                "end_date",
                "total_budget",
                "department",
                "program_manager",
                "priority",
            ]
        )

        for project_id in project_ids:
            name = f"Project {fake.catch_phrase()}"
            project_type = random.choice(PROJECT_TYPES)
            description = fake.paragraph(nb_sentences=3)

            # Project dates - typically 2-7 years
            start_year = random.randint(2015, 2022)
            start_date_obj = datetime.date(start_year, 1, 1)
            end_date_obj = datetime.date(start_year, 12, 31)
            start_date = fake.date_between(start_date=start_date_obj, end_date=end_date_obj)
            duration_years = random.randint(2, 7)
            end_date = start_date + datetime.timedelta(days=365 * duration_years)

            # Budget - large programs can be hundreds of millions
            total_budget = round(random.uniform(5000000, 500000000), 2)
            department = random.choice(DEPARTMENTS)
            program_manager = personnel_ids[random.randint(0, len(personnel_ids) - 1)]
            priority = random.choice(["Low", "Medium", "High", "Critical"])

            writer.writerow(
                [
                    project_id,
                    name,
                    project_type,
                    description,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    f"{total_budget:.2f}",
                    department,
                    program_manager,
                    priority,
                ]
            )

    print(f"✅ Generated {NUM_PROJECTS} projects")


def generate_transactions():
    """Generate financial transaction data"""
    print("Generating transaction data...")

    # Generate in chunks to avoid memory issues
    chunk_size = 10000
    num_chunks = (NUM_TRANSACTIONS + chunk_size - 1) // chunk_size

    with open(TRANSACTIONS_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "transaction_id",
                "contract_id",
                "transaction_date",
                "amount",
                "type",
                "description",
                "fiscal_year",
                "fiscal_quarter",
                "invoice_number",
                "approved_by",
            ]
        )

        transactions_written = 0

        for chunk in range(num_chunks):
            chunk_transactions = min(chunk_size, NUM_TRANSACTIONS - transactions_written)

            for _ in range(chunk_transactions):
                transaction_id = str(uuid.uuid4())
                contract_id = random.choice(contract_ids)

                # Get contract dates to make sure transaction is within contract period
                with open(CONTRACTS_FILE, "r", newline="") as f:
                    reader = csv.DictReader(f)
                    contract_data = next(
                        (row for row in reader if row["contract_id"] == contract_id), None
                    )

                if contract_data:
                    start_date = datetime.datetime.strptime(
                        contract_data["start_date"], "%Y-%m-%d"
                    )
                    end_date = datetime.datetime.strptime(contract_data["end_date"], "%Y-%m-%d")

                    # Generate transaction date within contract period
                    transaction_date = fake.date_between(start_date=start_date, end_date=end_date)

                    # Transaction amount based on contract value
                    contract_value = float(contract_data["current_value"])
                    max_transaction = (
                        contract_value * 0.1
                    )  # Max 10% of contract in one transaction
                    amount = round(random.uniform(1000, max_transaction), 2)

                    transaction_type = random.choice(TRANSACTION_TYPES)
                    description = fake.sentence()

                    # Calculate fiscal year and quarter (assuming Oct 1 start)
                    fiscal_year = (
                        transaction_date.year
                        if transaction_date.month >= 10
                        else transaction_date.year - 1
                    )
                    if transaction_date.month in (10, 11, 12):
                        fiscal_quarter = 1
                    elif transaction_date.month in (1, 2, 3):
                        fiscal_quarter = 2
                    elif transaction_date.month in (4, 5, 6):
                        fiscal_quarter = 3
                    else:
                        fiscal_quarter = 4

                    invoice_number = f"INV-{random.randint(10000, 99999)}"
                    approved_by = personnel_ids[random.randint(0, len(personnel_ids) - 1)]

                    writer.writerow(
                        [
                            transaction_id,
                            contract_id,
                            transaction_date.strftime("%Y-%m-%d"),
                            f"{amount:.2f}",
                            transaction_type,
                            description,
                            fiscal_year,
                            fiscal_quarter,
                            invoice_number,
                            approved_by,
                        ]
                    )

            transactions_written += chunk_transactions
            print(f"  Progress: {transactions_written}/{NUM_TRANSACTIONS} transactions")

    print(f"✅ Generated {NUM_TRANSACTIONS} transactions")


def generate_modifications():
    """Generate contract modification data"""
    print("Generating contract modification data...")

    with open(MODIFICATIONS_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "modification_id",
                "contract_id",
                "mod_number",
                "mod_date",
                "type",
                "description",
                "value_change",
                "days_change",
                "approved_by",
                "status",
            ]
        )

        for i in range(NUM_MODIFICATIONS):
            modification_id = f"MOD-{i+1:06d}"
            contract_id = random.choice(contract_ids)
            mod_number = f"P{random.randint(0, 9)}{random.randint(10, 99)}"

            # Get contract dates
            with open(CONTRACTS_FILE, "r", newline="") as f:
                reader = csv.DictReader(f)
                contract_data = next(
                    (row for row in reader if row["contract_id"] == contract_id), None
                )

            if contract_data:
                start_date = datetime.datetime.strptime(contract_data["start_date"], "%Y-%m-%d")
                end_date = datetime.datetime.strptime(contract_data["end_date"], "%Y-%m-%d")

                # Modification date during contract period
                mod_date = fake.date_between(start_date=start_date, end_date=end_date)

                mod_type = random.choice(MODIFICATION_TYPES)
                description = fake.paragraph(nb_sentences=1)

                # Value change could be positive or negative
                contract_value = float(contract_data["current_value"])
                if mod_type in ["Funding", "Scope Change", "Extension"]:
                    value_change = round(
                        random.uniform(-0.2 * contract_value, 0.3 * contract_value), 2
                    )
                else:
                    value_change = 0.0

                # Schedule change in days
                if mod_type in ["Schedule", "Extension"]:
                    days_change = random.randint(-30, 180)
                else:
                    days_change = 0

                approved_by = personnel_ids[random.randint(0, len(personnel_ids) - 1)]
                status = random.choice(["Approved", "Pending", "Rejected", "In Review"])

                writer.writerow(
                    [
                        modification_id,
                        contract_id,
                        mod_number,
                        mod_date.strftime("%Y-%m-%d"),
                        mod_type,
                        description,
                        f"{value_change:.2f}",
                        days_change,
                        approved_by,
                        status,
                    ]
                )

            if (i + 1) % 500 == 0:
                print(f"  Progress: {i + 1}/{NUM_MODIFICATIONS} modifications")

    print(f"✅ Generated {NUM_MODIFICATIONS} contract modifications")


def generate_deliverables():
    """Generate contract deliverable data"""
    print("Generating contract deliverable data...")

    with open(DELIVERABLES_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "deliverable_id",
                "contract_id",
                "title",
                "type",
                "due_date",
                "delivery_date",
                "status",
                "description",
                "accepted",
                "reviewer",
            ]
        )

        for i in range(NUM_DELIVERABLES):
            deliverable_id = f"DEL-{i+1:06d}"
            contract_id = random.choice(contract_ids)

            # Get contract dates
            with open(CONTRACTS_FILE, "r", newline="") as f:
                reader = csv.DictReader(f)
                contract_data = next(
                    (row for row in reader if row["contract_id"] == contract_id), None
                )

            if contract_data:
                start_date = datetime.datetime.strptime(contract_data["start_date"], "%Y-%m-%d")
                end_date = datetime.datetime.strptime(contract_data["end_date"], "%Y-%m-%d")

                # Deliverable due date during contract period
                due_date = fake.date_between(start_date=start_date, end_date=end_date)

                # Title and description
                title = f"Deliverable {fake.bs()}"
                deliverable_type = random.choice(DELIVERABLE_TYPES)
                description = fake.paragraph(nb_sentences=2)

                # Status and delivery date
                status_options = ["Pending", "Delivered", "Accepted", "Rejected", "Delayed"]
                status = random.choice(status_options)

                if status in ["Delivered", "Accepted", "Rejected"]:
                    # Delivery date - most on time, some late, few early
                    days_offset = random.choices(
                        [-10, -5, 0, 3, 7, 15, 30], weights=[5, 10, 60, 10, 8, 5, 2], k=1
                    )[0]
                    delivery_date = due_date + datetime.timedelta(days=days_offset)
                    delivery_date = delivery_date.strftime("%Y-%m-%d")

                    # For delivered items, set accepted status
                    accepted = (
                        random.choices(["Yes", "No", "Conditional"], weights=[80, 15, 5], k=1)[0]
                        if status == "Delivered"
                        else "N/A"
                    )
                else:
                    delivery_date = ""
                    accepted = "N/A"

                reviewer = personnel_ids[random.randint(0, len(personnel_ids) - 1)]

                writer.writerow(
                    [
                        deliverable_id,
                        contract_id,
                        title,
                        deliverable_type,
                        due_date.strftime("%Y-%m-%d"),
                        delivery_date,
                        status,
                        description,
                        accepted,
                        reviewer,
                    ]
                )

            if (i + 1) % 1000 == 0:
                print(f"  Progress: {i + 1}/{NUM_DELIVERABLES} deliverables")

    print(f"✅ Generated {NUM_DELIVERABLES} contract deliverables")


def generate_personnel():
    """Generate personnel data"""
    print("Generating personnel data...")

    with open(PERSONNEL_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "personnel_id",
                "name",
                "role",
                "department",
                "email",
                "phone",
                "security_clearance",
                "hire_date",
                "supervisor",
            ]
        )

        # Generate 1000 personnel records
        for personnel_id in personnel_ids:
            name = fake.name()
            role = random.choice(PERSONNEL_ROLES)
            department = random.choice(DEPARTMENTS)
            email = fake.email()
            phone = fake.phone_number()
            security_clearance = random.choice(
                ["Secret", "Top Secret", "TS/SCI", "Confidential", "Public Trust"]
            )
            hire_date = fake.date_between(start_date="-20y", end_date="today").strftime("%Y-%m-%d")

            # Some personnel are supervisors
            if random.random() < 0.8:  # 80% have a supervisor
                supervisor = personnel_ids[random.randint(0, len(personnel_ids) - 1)]
                # Avoid self-supervision
                while supervisor == personnel_id:
                    supervisor = personnel_ids[random.randint(0, len(personnel_ids) - 1)]
            else:
                supervisor = ""

            writer.writerow(
                [
                    personnel_id,
                    name,
                    role,
                    department,
                    email,
                    phone,
                    security_clearance,
                    hire_date,
                    supervisor,
                ]
            )

    print(f"✅ Generated {len(personnel_ids)} personnel records")


def generate_contract_data():
    """Generate all defense contract financial datasets"""
    print("Starting defense contract financial data generation...")

    # Generate all datasets
    generate_contracts()
    generate_vendors()
    generate_projects()
    generate_transactions()
    generate_modifications()
    generate_deliverables()
    generate_personnel()

    print("\nData generation complete! Files are in the 'data/raw' directory.")
    print("Summary:")
    print(f"- {NUM_CONTRACTS} contracts")
    print(f"- {NUM_VENDORS} vendors")
    print(f"- {NUM_PROJECTS} projects")
    print(f"- {NUM_TRANSACTIONS} financial transactions")
    print(f"- {NUM_MODIFICATIONS} contract modifications")
    print(f"- {NUM_DELIVERABLES} deliverables")
    print(f"- 1000 personnel records")

    # Provide some tips for scaling up
    print("\nTips for scaling the dataset:")
    print("1. Increase NUM_CONTRACTS, NUM_TRANSACTIONS, etc. in the configuration section")
    print("2. For larger datasets, adjust the chunk_size variables if you encounter memory issues")
