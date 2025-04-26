import json
from django.http import JsonResponse
from django.utils import timezone  # ✅ this one
from datetime import datetime, timedelta, date
import random
from .models import Employee, Medication, NurseNotes, PatientInformation, Shift_schedule, VitalSigns1, VitalSigns2
import time
import threading
from django.contrib.auth.models import User
from decimal import Decimal


# print("hello nurse")

# nurse_id =  ""
def get_patients(request):
    # global nurse_id 
    patients = PatientInformation.objects.all()
    patient_list = []
    nurse_id = request.session['user_id']
    # print(nurse_id)
    nurse_shift = Shift_schedule.get_nearest_shift_by_employee_id(nurse_id)
    # if nurse_shift:
    #     print(nurse_shift)
    # else:
    #     print("No shift found for today.")
    

    for patient in patients:
        patient_list.append({
            'id': patient.id,  # UUID field for patient ID
            'name': patient.name,  # Patient's full name
            'sex': patient.get_sex_display(),  # Human-readable sex using choices
            'birthday': patient.birthday.strftime("%Y-%m-%d"),  # Patient's birthdate formatted
            'phone_number': patient.phone_number,  # Patient's phone number
            'status': patient.get_status_display(),  # Human-readable status using choices
            'ward': patient.get_ward_display(),  # Human-readable ward using choices
            'qr_code': patient.qr_code.url if patient.qr_code else None,  # QR code URL or None
            'created_at': patient.created_at.strftime("%Y-%m-%d %H:%M"),  # Timestamp formatted
            'end_time': nurse_shift.end_time,
            
        })
    return JsonResponse({'patients': patient_list})


# Check if patient exist
def check_patient_id(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hospital_id = data.get('hospital_id')
            # print(hospital_id)
            if not hospital_id:
                return JsonResponse({'error': 'hospital_id is required'}, status=400)

            exists = PatientInformation.id_exists(hospital_id)
            print(exists)
            return JsonResponse({'exists': exists})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


import json
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import (
    PatientInformation,
    VitalSigns1,
    VitalSigns2,
    Medication,
    NurseNotes,
    Employee
)

# View to check patient existence
def check_patient_id(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hospital_id = data.get('hospital_id')
            if not hospital_id:
                return JsonResponse({'error': 'hospital_id is required'}, status=400)

            exists = PatientInformation.id_exists(hospital_id)
            return JsonResponse({'exists': exists})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# Function to create sample data
def create_sample_data():
    # Create 3 sample nurses with associated users
    nurse_data = [
        {
            "name": "Nurse Sarah Johnson",
            "username": "sarah.johnson",
            "employee_id": "EMP101",
            "role": "Registered Nurse",
            "email": "sarah.johnson@hospital.com",
            "phone_number": "09123456781",
            "sex": "F",
            "birthdate": datetime.now() - timedelta(days=30*365),
            "status": "Active"
        },
        {
            "name": "Nurse Michael Chen",
            "username": "michael.chen",
            "employee_id": "EMP102",
            "role": "Senior Nurse",
            "email": "michael.chen@hospital.com",
            "phone_number": "09123456782",
            "sex": "M",
            "birthdate": datetime.now() - timedelta(days=35*365),
            "status": "Active"
        },
        {
            "name": "Nurse Emily Davis",
            "username": "emily.davis",
            "employee_id": "EMP103",
            "role": "Pediatric Nurse",
            "email": "emily.davis@hospital.com",
            "phone_number": "09123456783",
            "sex": "F",
            "birthdate": datetime.now() - timedelta(days=28*365),
            "status": "Active"
        }
    ]

    nurses = []
    for data in nurse_data:
        # Create user account first
        user = User.objects.create_user(
            username=data["name"],
            email=data["email"],
            password="temp_password123"  # Change in production!
        )
        
        # Create employee record linked to the user
        nurse = Employee.objects.create(
            user=user,
            name=data["name"],
            employee_id=data["employee_id"],
            role=data["role"],
            email=data["email"],
            phone_number=data["phone_number"],
            sex=data["sex"],
            birthdate=data["birthdate"],
            status=data["status"]
            # master_key is intentionally left NULL
        ) 
        nurses.append(nurse)
    
    # Create 5 sample patients
    for i in range(1, 6):
        # Create patient
        patient = PatientInformation.objects.create(
            name=f"Patient {i}",
            sex=random.choice(["Male", "Female", "Other"]),
            birthday=datetime.now() - timedelta(days=random.randint(18*365, 80*365)),
            phone_number=f"09{random.randint(100000000, 999999999)}",
            status=random.choice(["Inpatient", "Outpatient", "Discharge"]),
            ward=random.choice(["General", "Pediatrics", "ICU", "Maternity", "None"]),
            physician_name=random.choice(["Dr. Smith", "Dr. Lee", "Dr. Garcia", "Dr. Wilson"])
        )
        
        # Create VitalSigns1 record
        VitalSigns1.objects.create(
            patient=patient,
            allergies=random.choice([
                "Penicillin",
                "Sulfa drugs",
                "NSAIDs",
                "No known allergies",
                "Peanuts, Shellfish"
            ]),
            family_history=random.choice([
                "Hypertension, Diabetes",
                "Cardiac disease",
                "Cancer - breast and colon",
                "No significant family history",
                "Asthma, Allergies"
            ]),
            physical_exam=random.choice([
                "Normal exam",
                "Hypertensive on exam",
                "Lungs clear to auscultation",
                "Abdomen soft, non-tender",
                "Edema in lower extremities"
            ]),
            diagnosis=random.choice([
                "Community-acquired pneumonia",
                "Hypertension",
                "Type 2 Diabetes",
                "UTI",
                "COPD exacerbation"
            ])
        )
        
        # Create 2-3 VitalSigns2 records per patient
        for _ in range(random.randint(2, 3)):
            VitalSigns2.objects.create(
                patient=patient,
                temperature=round(random.uniform(36.0, 39.5), 1),
                blood_pressure=f"{random.randint(90, 140)}/{random.randint(60, 90)}",
                pulse_rate=random.randint(60, 100),
                respiratory_rate=random.randint(12, 20),
                oxygen_saturation=round(random.uniform(95.0, 100.0), 1)
            )
        
        # Create 1-3 medications per patient
        medications = [
            ("Paracetamol", 500, "mg", "qid", "oral", 7),
            ("Amoxicillin", 500, "mg", "tid", "oral", 10),
            ("Losartan", 50, "mg", "daily", "oral", 30),
            ("Salbutamol", 2, "puff", "prn", "inhalation", 30),
            ("Metformin", 1000, "mg", "bid", "oral", 30)
        ]
        
        for med in random.sample(medications, random.randint(1, 3)):
            Medication.objects.create(
                patient=patient,
                drug_name=med[0],
                dose=med[1],
                units=med[2],
                frequency=med[3],
                route=med[4],
                duration=med[5],
                quantity=random.randint(10, 60),
                start_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                status=random.choice(["active", "completed", "inactive"]),
                patient_instructions=f"Take {med[1]}{med[2]} {med[3]} for {med[5]} days"
            )
        
        # Create 2-4 nurse notes per patient
        for _ in range(random.randint(2, 4)):
            NurseNotes.objects.create(
                patient=patient,
                nurse=random.choice(nurses),
                notes=random.choice([
                    "Patient resting comfortably",
                    "Administered scheduled medications",
                    "Vital signs stable",
                    "Patient complained of mild headache - given paracetamol",
                    "Dressing changed - wound healing well",
                    "Patient educated on medication administration",
                    "No complaints at this time",
                    "Family visited, patient in good spirits"
                ])
            )
    
    print("Successfully created sample data including:")
    print(f"- {len(nurses)} nurse employees with user accounts")
    print("- 5 patient records with complete medical data")
    return {
        "nurses": nurses,
        "patients": PatientInformation.objects.order_by('-id')[:5]
    }
    
# create_sample_data()






