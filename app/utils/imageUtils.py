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
    separator_width = separator_image.width    
    total_width = sum(img.width for img in cropped_images) + (len(cropped_images) - 1) * separator_width
    print("Total Width:", total_width)
    
    max_height = max(max(img.height for img in cropped_images), separator_image.height)
    print("Max Height:", max_height)
    
    combined_image = Image.new('RGB', (total_width, max_height))
    x = 0
    print(cropped_images, "before combine")
    for i, img in enumerate(cropped_images):
        combined_image.paste(img, (x, 0))
        x += img.width
        if i < len(cropped_images) - 1:
            combined_image.paste(separator_image, (x, 0))
            x += separator_width
    combined_image.save("combinedImage.png")
    return combined_image

def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary)