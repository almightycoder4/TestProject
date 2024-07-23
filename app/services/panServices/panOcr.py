from io import BytesIO
from ...utils.azureOCR import analyze_image
from ...utils.imageUtils import resize_if_needed, all_cropped_images_to_one_image
from .panDataExtractor import extract_panData
# from collections import defaultdict

def process_results(results, img):
    label_indices = {"pan_num": 0, "name": 1, "father": 2, "dob": 3}
    confidence_threshold = 0.3
    input_image_format = img.format if img.format else "PNG"
    valid_formats = ["JPEG", "PNG", "BMP", "GIF", "TIFF"]
    input_image_format = input_image_format if input_image_format in valid_formats else "PNG"
    
    best_crops = {label: (None, -1) for label in label_indices.keys()}  # Store best (image, confidence) pairs

    precision_data = {label: {"correct": 0, "total": 0} for label in label_indices.keys()}
    
    for result in results:
        for bbox, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
            # Ensure the class index is within the bounds of the label list
            if int(cls) >= len(label_indices):
                print(f"Warning: Class index {cls} is out of range. Skipping this bbox.")
                continue
            
            label = list(label_indices.keys())[int(cls)]
            print(label, conf)
            if conf < confidence_threshold:
                continue

            x1, y1, x2, y2 = map(int, bbox.tolist())
            crop_img = img.crop((x1, y1, x2, y2))
            crop_img = resize_if_needed(crop_img)
            crop_img.save(f"temp_{label}.png")

            # Replace old crop if new one has higher confidence
            _, best_conf = best_crops[label]
            if conf > best_conf:
                best_crops[label] = (crop_img, conf)
                precision_data[label]["total"] += 1
                precision_data[label]["correct"] += 1  # Replace with actual OCR validation check

    # Extract the images for final processing
    cropped_images_with_labels = [(img, label_indices[label], conf) for label, (img, conf) in best_crops.items() if img is not None]
    
    # Sort the images by their label indices in ascending order
    cropped_images_with_labels.sort(key=lambda x: x[1])
    print(cropped_images_with_labels, "cropped images with labels")
    
    if not cropped_images_with_labels:
        raise ValueError("No images were cropped.")

    # Extract only the images for concatenation
    cropped_images = [img for img, _, _ in cropped_images_with_labels]
    
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