import torch
from ultralytics import YOLO
import cv2
from PIL import Image
import requests
from io import BytesIO
import os
import numpy as np
import glob
import pytesseract
from openbharatocr.ocr.aadhaar import extract_aadhaar, extract_dob, extract_name, extract_gender, extract_address, extract_fathers_name
# Load the YOLOv8 model
model = YOLO('aadhaar.pt')

def clear_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    files = glob.glob(os.path.join(directory, '*'))
    for f in files:
        os.remove(f)
    print(f"Cleared {directory} directory.")

def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def detect_and_crop(image_url, model, output_dir='./tmp'):
    # Clear the output directory
    clear_directory(output_dir)
    
    # Download image
    image = download_image(image_url)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Perform detection
    results = model(image_cv)
    
    extracted_data = {}
    
    label_map = {
        0: "aadharNo",
        1: "dob",
        2: "gender",
        3: "name",
        4: "address"
    }
    
    # Iterate over detected objects
    for i, result in enumerate(results):
        boxes = result.boxes  # This holds the bounding boxes
        for j, box in enumerate(boxes):
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0])
            label_index = int(box.cls)
            label = label_map.get(label_index, f"label_{label_index}")
            cropped_img = image.crop((x_min, y_min, x_max, y_max)).convert('RGB')
            
            # Define the output file path
            output_path = os.path.join(output_dir, f"{label}_{i}_{j}.jpg")
            
            # Save the cropped image
            cropped_img.save(output_path)
            print(f"Saved cropped image: {output_path}")
            
            try:
                # Perform OCR on the cropped image
                custom_config = r'--oem 3 --psm 6'
                ocr_result = pytesseract.image_to_string(output_path, lang='eng', config=custom_config).strip()
                if label == "aadharNo":
                    ocr_result = extract_aadhaar(ocr_result)
                
                if label == "name":
                    ocr_result = extract_name(ocr_result)
                
                if label == "fathersName":
                    ocr_result = extract_fathers_name(ocr_result)
                
                if label == "dob":
                    ocr_result = extract_dob(ocr_result)
                
                extracted_data[label] = ocr_result.replace('\n', ' ')
                print(f"OCR result for {label}: {ocr_result}")
            except pytesseract.TesseractError as e:
                print(f"Error during OCR for {output_path}: {e}")
                error_message = e.stderr.decode('utf-8', errors='ignore')
                print(f"Tesseract error details: {error_message}")
                extracted_data[label] = ""
    
    return extracted_data

def main():
    # Ask user for image URL
    image_url = input("Enter the URL of the image: ")
    
    # Detect and crop the labeled boxes, then perform OCR
    extracted_data = detect_and_crop(image_url, model)
    
    print("Extracted Data:")
    print(extracted_data)

if __name__ == "__main__":
    main()
