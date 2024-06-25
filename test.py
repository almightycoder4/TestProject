import requests
from openbharatocr.ocr.voter_id import voter_id_front, voter_id_back, extract_voterid_details_front

def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image successfully downloaded to {file_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None
    return file_path

def process_pan_image(image_url):
    # Define the local file path where the image will be saved
    file_path = 'downloaded_image.jpg'
    
    # Download the image
    image_path = download_image(image_url, file_path)
    
    if image_path:
        # Process the downloaded image using openbharatocr
        dict_output = voter_id_front(image_path)
        # Print the output
        print(dict_output)
    else:
        print("Image processing skipped due to download failure.")

# Ask the user to input the URL of the image
image_url = input("Please enter the URL of the PAN card image: ")
process_pan_image(image_url)
