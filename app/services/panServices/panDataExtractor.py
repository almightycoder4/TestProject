import re
def filter_array(arr):
    # Define the regex patterns
    pattern_alphanumeric_special = re.compile(r'[\w]+[^.\s\w]+|[^.\s\w]+[\w]+')
    pattern_numeric = re.compile(r'^[0-9]+$')
    pattern_non_alpha = re.compile(r'[^.\s]*[^a-zA-Z\s][^.\s]*')
    
    # Filter the array
    filtered_array = [
        item for item in arr 
        if not (pattern_alphanumeric_special.search(item) or 
                pattern_numeric.match(item) or 
                pattern_non_alpha.search(item))
    ]
    return filtered_array

def extract_panData(data):
    unwanted_words = ["Name", "/Name", 'Permanent', 'Account', 'Number', 'Card', 'नाम', '/Name',
                      "पिता का नाम", 'नाम / Name', "पिता का नाम/ Father's Name", '414 / Name', 'पिता का नाम / Fath', 
                      "VIT VE Hra / Father's Nama", 'पिता का नाम/ Fal', 'पिता का नाम / Fathe', "पिता का नाम / Father's Na", 
                      'जन्म की तारीख /।', 'जन्म का ताराख', "पिता का नाम/ Father's Nam", 'नाम /Name', "पिता का नाम / Father's Name", 
                      'जन्म का वाराज़', 'Date of Birth', 'Permanent Account Number Card', "Date of Birth", "/Date of Birth", 
                      "Permanent Account Number", "Father's Name", "14 /Name", "/Father's Name", 'HTH / Name']
    

    
    
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
    
    # Clean the array by removing unwanted words and invalid entries
    cleaned_data = []
    combination_pattern = re.compile(r'(?=.*[0-9])(?=.*[!@#$%^&*(),?":{}|<>])')

    for item in data:
        if item not in unwanted_words and not combination_pattern.search(item):
            cleaned_data.append(item)
    
   
    # Check and extract PAN number
    pan_pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
    for item in cleaned_data:
        if pan_pattern.match(item):
            result["data"]["panNo"] = item
            cleaned_data.remove(item)
            break
    
    # Check and extract date of birth
    dob_pattern = re.compile(r'^\d{2}[-/]\d{2}[-/]\d{4}$')
    for item in cleaned_data:
        if dob_pattern.match(item):
            result["data"]["dob"] = item
            cleaned_data.remove(item)
            break

    # If only two values are left, assume they are name and father's name
    cleaned_data = filter_array(cleaned_data)
    if len(cleaned_data) == 2:
        result["data"]["name"] = cleaned_data[0]
        result["data"]["fatherName"] = cleaned_data[1]
    else:
        # Further cleaning of the data array to extract name and father's name
        cleaned_data = [item for item in cleaned_data if not combination_pattern.search(item) and item not in unwanted_words]
        print(cleaned_data, "after cleaning")
        # Check and extract name
        name_pattern = re.compile(r'^[A-Za-z .]+$')
        if len(cleaned_data) > 0 and name_pattern.match(cleaned_data[0]):
            result["data"]["name"] = cleaned_data[0]
        else:
            result["data"]["name"] = ''
            
        # Check and extract father's name
        if len(cleaned_data) > 1 and name_pattern.match(cleaned_data[1]):
            result["data"]["fatherName"] = cleaned_data[1]
        else:
            result["data"]["fatherName"] = ''
    
    # Check if any value is empty and set error message
    for key, value in result["data"].items():
        if value == '':
            result["statusCode"] = 400
            result["error"] = f"{key} value is not found due to bad image."
            break
    
    return result
