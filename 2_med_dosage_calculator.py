#!/usr/bin/env python3
"""
Emergency Room Medication Calculator

This script calculates medication dosages for emergency room patients based on 
standard emergency protocols. It follows weight-based dosing guidelines for common 
emergency medications.

Dosing Formula:
    Base Dosage (mg) = Patient Weight (kg) × Medication Factor (mg/kg)
    Loading Dose (mg) = Base Dosage × 2 (for first dose only)

When to use Loading Doses:
    - Only for first doses of certain medications (e.g., antibiotics, anti-seizure meds)
    - Determined by 'is_first_dose' flag in the input
    - Some medications always use loading doses for first administration

Example:
    Patient: 70kg, Medication: epinephrine, Is First Dose: No
    Base Dosage = 70 kg × 0.01 mg/kg = 0.7 mg
    Final Dosage = 0.7 mg

    Patient: 70kg, Medication: amiodarone, Is First Dose: Yes
    Base Dosage = 70 kg × 5 mg/kg = 350 mg
    Loading Dose = 350 mg × 2 = 700 mg
    Final Dosage = 700 mg

Input Format:
    {
        "name": "John Smith",
        "weight": 70.0,
        "medication": "epinephrine",
        "condition": "anaphylaxis",
        "is_first_dose": false,
        "allergies": ["penicillin"]
    }

Output:
    {
        "name": "John Smith",
        "weight": 70.0,
        "medication": "epinephrine",
        "base_dosage": 0.7,
        "is_first_dose": false,
        "loading_dose_applied": false,
        "final_dosage": 0.7,
        "warnings": ["Monitor for arrhythmias"]
    }

Medication Factors (mg/kg):
    epinephrine:  0.01  (Anaphylaxis)
    amiodarone:   5.00  (Cardiac arrest)
    lorazepam:    0.05  (Seizures)
    fentanyl:     0.001 (Pain)
    ...
"""

import json
import os

# Dosage factors for different medications (mg per kg of body weight)
# These are standard dosing factors based on medical guidelines
DOSAGE_FACTORS = {
    "epinephrine": 0.01,  # Anaphylaxis
    "amiodarone": 5.00,   # Cardiac arrest
    "lorazepam": 0.05,    # Seizures
    "fentanyl": 0.001,    # Pain
    "lisinopril": 0.5,    # ACE inhibitor for blood pressure
    "metformin": 10.0,    # Diabetes medication
    "oseltamivir": 2.5,   # Antiviral for influenza
    "sumatriptan": 1.0,   # Migraine medication
    "albuterol": 0.1,     # Asthma medication
    "ibuprofen": 5.0,     # Pain/inflammation
    "sertraline": 1.5,    # Antidepressant
    "levothyroxine": 0.02 # Thyroid medication
}

# Medications that use loading doses for first administration
# BUG: Missing commas between list items
# FIX: fixed list syntax
# BUG: typo in fentanyl
# FIX: fixed typo
LOADING_DOSE_MEDICATIONS = [
    "amiodarone",
    "lorazepam",
    "fentanyl",
]

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    # BUG: No error handling for file not found
    # FIX: Added a try except block to catch errors while loading
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load patient data: {e}")
        return []

def calculate_dosage(patient):
    """
    Calculate medication dosage for a patient.
    
    Args:
        patient (dict): Patient dictionary with 'weight', 'medication', and 'is_first_dose' keys
        
    Returns:
        dict: Patient dictionary with added dosage information
        # BUG: The tests are asserting:
            assert expected_dosage (int) == calculate_dosage(patient)
            So our output should be of type int and not dict
        # FIX: Return the final_dosage instead
    """
    # Create a copy of the patient data to avoid modifying the original
    patient_with_dosage = patient.copy()
    
    # Extract patient information
    # BUG: No check if 'weight' key exists
    # FIX: If the weight key Does Not Exist .get() will return None for weight
    weight = patient.get('weight')

    # BUG: No check if 'medication' key exists
    # FIX: if the medication key Does Not Exist .get() will return None for medication    
    medication = patient.get('medication')
    
    # Get the medication factor
    # BUG: Adding 's' to medication name, which doesn't match DOSAGE_FACTORS keys
    # FIX: now we look up the DOSAGE_FACTORS dict for medication and if we don't have that key we dose 0
    # FIX: removed unnecessarily adding 's' to the medication name
    factor = DOSAGE_FACTORS.get(medication, 0)
    
    # Calculate base dosage
    # BUG: Using addition instead of multiplication
    # FIX: Code now uses correct formula for dosage
    base_dosage = weight * factor
    
    # Determine if loading dose should be applied
    # BUG: No check if 'is_first_dose' key exists
    # FIX: using .get() checks for the is_first_dose key and if it doesn't exist it will be set to False
    # final dose is the base dosage unless we need a loading dose
    # if its a first dose and loading dose, final dosage = 2 * base dosage
    is_first_dose = patient.get('is_first_dose', False)
    loading_dose_applied = False
    final_dosage = base_dosage
    
    # Apply loading dose if it's the first dose and the medication uses loading doses
    
    # BUG: Incorrect condition - should check if medication is in LOADING_DOSE_MEDICATIONS
    # FIX: Updated if statement to equivalent nested if statement
 
    # BUG: Using addition instead of multiplication for loading dose
    # FIX: Updated formula to use multiplication
        
    if is_first_dose:
        if medication in LOADING_DOSE_MEDICATIONS:
            final_dosage = base_dosage * 2
            loading_dose_applied = True


    # BUG: This section is not needed in this function
    # FIX: Commented this code out
        
    # # Add dosage information to the patient record
    # patient_with_dosage['base_dosage'] = base_dosage
    # patient_with_dosage['loading_dose_applied'] = loading_dose_applied
    # patient_with_dosage['final_dosage'] = final_dosage
    
    # BUG: The section: "Add warnings based on medication" fits better in calculate_all_dosages function
    # FIX: Moved the warnings section
    
    
    # BUG: initiall returned dictionary however the tests assert that the output is of type int and is the expected final dosage
    # FIX: updated to return final_dosage
    return final_dosage

def calculate_all_dosages(patients):
    """
    Calculate dosages for all patients and sum the total.
    
    Args:
        patients (list): List of patient dictionaries
        
    Returns:
        tuple: (list of patient dicts with dosages, total medication needed)
    """
    total_medication = 0
    patients_with_dosages = []
    
    # Process all patients
    for patient in patients:
        # Calculate dosage for this patient
        # BUG: Updated calculate_dosage to return dosage as a number
        # FIX: Since the test expects a list of 3 patients each with a dosage key, we will update the list: patients_with_dosages accordingly
        # FIX: Since we need each dosage to calculate total_medication, we store it as a variable
        patient_with_dosage = patient.copy()
        temp_dosage = calculate_dosage(patient_with_dosage)
        patient_with_dosage["dosage"] = temp_dosage
        patient_with_dosage["final_dosage"] = temp_dosage
        
        weight = patient_with_dosage.get('weight')
        medication = patient_with_dosage.get('medication')
        factor = DOSAGE_FACTORS.get(medication, 0)
        base_dosage = weight * factor
        patient_with_dosage["base_dosage"] = base_dosage
        
        # Add warnings based on medication
        warnings = []

        # BUG: Typos in medication names
        # FIX: fixed typos
        if medication == "epinephrine":
            warnings.append("Monitor for arrhythmias")
        elif medication == "amiodarone":
            warnings.append("Monitor for hypotension")
        elif medication == "fentanyl":
            warnings.append("Monitor for respiratory depression")

        patient_with_dosage['warnings'] = warnings

        
        # Add to our list
        patients_with_dosages.append(patient_with_dosage)
        
        # Add to total medication
        # BUG: No check if 'final_dosage' key exists
        # FIX: This error no longer exists
        
        # BUG: Need to update the logic for total medication
        # FIX: Use temp_dosage for total_medication
        total_medication += temp_dosage

    return patients_with_dosages, total_medication

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'meds.json')
    
    # BUG: No error handling for load_patient_data failure
    # FIX: Error handling is present in the function and added more error hanling
    try:
        patients = load_patient_data(data_path)
        if not patients:
            raise ValueError("No patient data found.")
    except Exception as e:
        print(f"Error loading patient data: {e}")

    # Calculate dosages for all patients
    patients_with_dosages, total_medication = calculate_all_dosages(patients)
    
    # Print the dosage information
    print("Medication Dosages:")
    for patient in patients_with_dosages:
        # BUG: No check if required keys exist
        # fixed, using .get() to obtain the keys before printing and assigning the values to be None by default
        print(f"Name: {patient.get('name')}, Medication: {patient.get('medication')}, "
              f"Base Dosage: {patient.get('base_dosage'):.2f} mg, "
              f"Final Dosage: {patient.get('final_dosage'):.2f} mg")
        if patient.get('loading_dose_applied'):
            print(f"  * Loading dose applied")
        if patient.get('warnings'):
            print(f"  * Warnings: {', '.join(patient['warnings'])}")
    
    print(f"\nTotal medication needed: {total_medication:.2f} mg")
    
    # Return the results (useful for testing)
    return patients_with_dosages, total_medication

if __name__ == "__main__":
    main()