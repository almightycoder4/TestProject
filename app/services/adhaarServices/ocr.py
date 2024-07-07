from io import BytesIO
from ...utils.azureOCR import analyze_image
from ...utils.imageUtils import resize_if_needed, all_cropped_images_to_one_image
from app.services.adhaarServices.adhaarDataExtractor import extract_details

def process_results(results, img):
    precision_data = {label: {"correct": 0, "total": 0} for label in ["aadharNo", "name", "dob", "gender", "address"]}
    confidence_threshold = 0.3
    input_image_format = img.format if img.format else "PNG"
    valid_formats = ["JPEG", "PNG", "BMP", "GIF", "TIFF"]
    input_image_format = input_image_format if input_image_format in valid_formats else "PNG"
    
    label_to_image = {}
    extracted_data = {"adhaarNo": "", "dob": "", "gender": "", "name": "", "address": ""}
    for result in results:
        for bbox, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
            label = ["aadharNo", "dob", "gender", "name", "address"][int(cls)]
            print(label, conf)
            if conf < confidence_threshold or label == "address":
                continue
            
            x1, y1, x2, y2 = map(int, bbox.tolist())
            crop_img = img.crop((x1, y1, x2, y2))
            crop_img = resize_if_needed(crop_img)
            
            if label not in label_to_image or label_to_image[label][1] < conf:
                label_to_image[label] = (crop_img, conf)
                precision_data[label]["total"] += 1
                precision_data[label]["correct"] += 1  # Replace with actual OCR validation check

    cropped_images = [img for label, (img, conf) in sorted(label_to_image.items()) if label != "address"]
    final_image = all_cropped_images_to_one_image(cropped_images, separator_image_path='app/utils/seprator3.png')
    
    buffer = BytesIO()
    final_image.save(buffer, format=input_image_format)
    buffer.seek(0)
    
    response = analyze_image(buffer.getvalue(), input_image_format)
    # print(response)
    lines = response['readResult']['blocks'][0]['lines']
    texts = [line['text'] for line in lines]
    print(texts)
    extracted_data = extract_details(texts)
    return extracted_data