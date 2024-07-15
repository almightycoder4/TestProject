from PIL import Image
import cv2
import numpy as np

def resize_if_needed(image):
    width, height = image.size
    if width < 50 or height < 50:
        scale = max(70 / width, 70 / height)
    elif width > 16000 or height > 16000:
        scale = min(16000 / width, 16000 / height)
    else:
        return image
    return image.resize((int(width * scale), int(height * scale)), Image.LANCZOS)

def center_on_white_background(image):
    width, height = image.size
    if width < 150 and height < 50:
        background = Image.new('RGB', (150, 150), (255, 255, 255))
        x, y = (150 - width) // 2, (150 - height) // 2
        background.paste(image, (x, y))
        return background
    return image

def all_cropped_images_to_one_image(cropped_images, separator_image_path):
    separator_image = Image.open(separator_image_path)
    separator_height = separator_image.height
    
    total_height = sum(img.height for img in cropped_images) + (len(cropped_images) - 1) * separator_height
    print("Total Height:", total_height)
    
    max_width = max(max(img.width for img in cropped_images), separator_image.width)
    print("Max Width:", max_width)
    
    combined_image = Image.new('RGB', (max_width, total_height))
    y = 0
    print(cropped_images, "before combine")
    
    for i, img in enumerate(cropped_images):
        combined_image.paste(img, (0, y))
        y += img.height
        if i < len(cropped_images) - 1:
            combined_image.paste(separator_image, (0, y))
            y += separator_height
    
    combined_image.save("combinedImage.png")
    return combined_image

def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary)