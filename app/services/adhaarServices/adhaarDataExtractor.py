import datetime

def extract_details(texts):
    details = {'name': '', 'gender': '', 'dob': '', 'aadhaarNo': ''}
    
    current_year = datetime.datetime.now().year
    
    for text in texts:
        # Check if colon exists in text and split accordingly
        if ':' in text:
            text = text.split(':')[1].strip()

        cleaned_text = text.replace(':', '').strip()
        
        # Remove leading non-alphabetic characters for gender detection and strip spaces
        cleaned_gender = cleaned_text.lstrip('.-/').strip()
        
        # Check if the text is the name (only alphabets, spaces, and possibly dots)
        if (all(char.isalpha() or char.isspace() or char == '.' for char in cleaned_text) 
                and cleaned_gender.lower() not in ['male', 'female']):
            details['name'] = cleaned_text

        # Check if the text is the DOB (format: dd/mm/yyyy or yyyy)
        elif (len(cleaned_text) == 4 and 
              cleaned_text.isdigit() and 
              1900 < int(cleaned_text) < current_year):
            details['dob'] = cleaned_text

        # Check if the text is the DOB (format: dd/mm/yyyy or dd-mm-yyyy)
        elif (len(cleaned_text) == 10 and 
              (cleaned_text[2] in ['/', '-']) and 
              (cleaned_text[5] in ['/', '-']) and 
              cleaned_text.replace('/', '').replace('-', '').isdigit()):
            details['dob'] = cleaned_text

        # Check if the text is the gender (either 'Male' or 'Female')
        elif cleaned_gender.lower() in ['male', 'female']:
            details['gender'] = cleaned_gender.capitalize()

        # Check if the text is the Aadhaar number (12 digits after removing spaces)
        elif cleaned_text.replace(' ', '').isdigit() and len(cleaned_text.replace(' ', '')) == 12:
            details['aadhaarNo'] = cleaned_text
    
    # Check if any key's value is empty
    if any(value == '' for value in details.values()):
        error_key = next(key for key, value in details.items() if value == '')
        result = {
            'statusCode': 400,
            'result': details,
            'error': f'{error_key} value is not found due to bad image.'
        }
    else:
        result = {
            'statusCode': 200,
            'result': details,
            'error': ''
        }
    
    return result
