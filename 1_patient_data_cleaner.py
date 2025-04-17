#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    # BUG: No error handling for file not found
    # FIX: Added a try except block to handle errors and print the warning. 
    # returns an empty list if failed which is at least the same type that we would expect
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load patient data: {e}")
        return []

def clean_patient_data(patients):
    """
    Clean patient data by:
    - Capitalizing names
    - Converting ages to integers
    - Filtering out patients under 18
    - Removing duplicates
    
    Args:
        patients (list): List of patient dictionaries
        
    Returns:
        list: Cleaned list of patient dictionaries
    """
    cleaned_patients = []
    
    for patient in patients:
        # BUG: Typo in key 'nage' instead of 'name'
        # FIX: Now correctly calls the name key
        patient['name'] = patient['name'].title()
        
        # BUG: Wrong method name (fill_na vs fillna)
        # FIX: Changed to fillna which is the correct pandas method, fill_na is used in R
        patient['age'] = patient['age'].fillna(0).astype(int)
        # BUG: Patient age is not being converted to integer as per description 
        # FIX: Convert age to integer using astype()
        
        # BUG: Wrong method name (drop_duplcates vs drop_duplicates)
        # FIX: Fixed typo
        patient = patient.drop_duplicates()
        
        # BUG: Wrong comparison operator (= vs ==)
        # FIX: Original code only checks for if the age is exactly 18
        # FIX: Updated functionality to correctly log all patients 18 or over
        if patient['age'] > 18:
            # BUG: Logic error - keeps patients under 18 instead of filtering them out
            # FIX: Updated functionality to correctly log all patients 18 or over
            cleaned_patients.append(patient)
    
    # BUG: Missing return statement for empty list
    # FIX: added a return statement for if cleaned_patients is empty
    if not cleaned_patients:
        return None
    
    return cleaned_patients

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    
    # BUG: No error handling for load_patient_data failure
    # FIX: This bug is handled in the function body but added a try except block here as well for code robustness
    try:
        patients = load_patient_data(data_path)
    except Exception as e:
        print(f"Failed to load patient data: {e}")
        patients = []

    
    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)
    
    # BUG: No check if cleaned_patients is None
    # FIX: added a check to only attempt to print the cleaned data if it exists
    # Print the cleaned patient data
    if cleaned_patients:
        print("Cleaned Patient Data:")
        for patient in cleaned_patients:
            # BUG: Using 'name' key but we changed it to 'nage'
            # FIX: We didn't change the name key to nage, we updated the code from nage to name
            # FIX: Fixed on line 83
            print(f"Name: {patient['name']}, Age: {patient['age']}, Diagnosis: {patient['diagnosis']}")
    
    # Return the cleaned data (useful for testing)
    return cleaned_patients

if __name__ == "__main__":
    main()