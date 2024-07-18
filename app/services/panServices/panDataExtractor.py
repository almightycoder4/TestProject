import re

def extract_panData(data):
    unwanted_words = ["Name","/Name",'Permanent', 'Account', 'Number', 'Card', 'नाम', '/Name',
        "पिता का नाम",'नाम / Name', "पिता का नाम/ Father's Name", "पिता का नाम/ Father's Nam", 'नाम /Name',"पिता का नाम / Father's Name", 'जन्म का वाराज़', 'Date of Birth', 'Permanent Account Number Card', "Date of Birth", "/Date of Birth", "Permanent Account Number", "Father's Name", "14 /Name", "/Father's Name"]
    
    # Clean the array by removing unwanted words and invalid entries
    cleaned_data = []
    combination_pattern = re.compile(r'(?=.*[A-Za-z])(?=.*[0-9])(?=.*[!@#$%^&*(),?":{}|<>])')

    for item in data:
        if item not in unwanted_words and not combination_pattern.search(item):
            cleaned_data.append(item)
    
    # Initialize result object
    result = {
        "statusCode": 200,
        "error": '',
        "data": {
            "panNo": '',
            "name": '',
            "fatherName": '',
            "dob": ''
        }
    }
    
    # Check and extract PAN number
    print(cleaned_data, "cleaned data")
    pan_pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
    if len(cleaned_data) > 0 and pan_pattern.match(cleaned_data[0]):
        result["data"]["panNo"] = cleaned_data[0]
    else:
        result["data"]["panNo"] = ''
        
    # Check and extract name
    name_pattern = re.compile(r'^[A-Za-z .]+$')
    if len(cleaned_data) > 1 and name_pattern.match(cleaned_data[1]):
        result["data"]["name"] = cleaned_data[1]
    else:
        result["data"]["name"] = ''
        
    # Check and extract father's name
    if len(cleaned_data) > 2 and name_pattern.match(cleaned_data[2]):
        result["data"]["fatherName"] = cleaned_data[2]
    else:
        result["data"]["fatherName"] = ''
        
    # Check and extract date of birth
    dob_pattern = re.compile(r'^\d{2}[-/]\d{2}[-/]\d{4}$')
    if len(cleaned_data) > 3 and dob_pattern.match(cleaned_data[3]):
        result["data"]["dob"] = cleaned_data[3]
    else:
        result["data"]["dob"] = ''
    
    # Check if any value is empty and set error message
    for key, value in result["data"].items():
        if value == '':
            result["statusCode"] = 400
            result["error"] = f"{key} value is not found due to bad image."
            break
    
    return result
