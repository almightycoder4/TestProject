from io import BytesIO
from ...utils.azureOCR import analyze_image
from ...utils.imageUtils import resize_if_needed, all_cropped_images_to_one_image
from .panDataExtractor import extract_panData

def process_results(results, img):
    label_indices = {"dob": 0, "father": 1, "name": 2, "pan_num": 3}
    confidence_threshold = 0.3
    input_image_format = img.format if img.format else "PNG"
    valid_formats = ["JPEG", "PNG", "BMP", "GIF", "TIFF"]
    input_image_format = input_image_format if input_image_format in valid_formats else "PNG"
    
    cropped_images_with_labels = []
    precision_data = {label: {"correct": 0, "total": 0} for label in label_indices.keys()}
    # extracted_data = {"pan_num": "", "name": "", "father": "", "dob": ""}
    
    for result in results:
        for bbox, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
            label = ["dob", "father", "name", "pan_num"][int(cls)]
            print(label, conf)
            if conf < confidence_threshold:
                continue
            
            x1, y1, x2, y2 = map(int, bbox.tolist())
            crop_img = img.crop((x1, y1, x2, y2))
            crop_img = resize_if_needed(crop_img)
            crop_img.save(f"temp_{label}.png")
            cropped_images_with_labels.append((crop_img, label_indices[label], conf))
            precision_data[label]["total"] += 1
            precision_data[label]["correct"] += 1  # Replace with actual OCR validation check
    
    # Sort the images by their label indices in ascending order
    cropped_images_with_labels.sort(key=lambda x: x[1])
    print(cropped_images_with_labels, "cropped images with labels")
    # Extract only the images for concatenation
    cropped_images = [img for img, _, _ in cropped_images_with_labels]
    # print(cropped_images, "cropped images")
    if not cropped_images:
        raise ValueError("No images were cropped.")
    
    final_image = all_cropped_images_to_one_image(cropped_images, separator_image_path='app/utils/seprator3.png')
    buffer = BytesIO()
    final_image.save(buffer, format=input_image_format)
    buffer.seek(0)
    
    response = analyze_image(buffer.getvalue(), input_image_format)
    print(response, "response")
    lines = response['readResult']['blocks'][0]['lines']
    texts = [line['text'] for line in lines]
    print(texts, "text after microsoft ocr")
    extracted_data = extract_panData(texts)
    return extracted_data
