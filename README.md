# Aadhaar OCR API

## Setup

1. Clone the repository.
2. Navigate to the project directory.
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Place the `aadhaar.pt` model file in the `models` directory.
5. Run the application:
    ```bash
    python run.py
    ```

## API

### `/aadhaarOcr`

- **Method**: POST
- **Description**: Perform OCR on Aadhaar card image.
- **Request Body**:
    ```json
    {
        "imgUrl": "URL of the image"
    }
    ```
- **Response**:
    ```json
    {
        "extractedData": {
            "aadharNo": "OCR result of image label 0",
            "name": "OCR result of image label 3",
            "dob": "OCR result of image label 1",
            "gender": "OCR result of image label 2",
            "address": "OCR result of image label 4"
        }
    }
    ```

## License

This project is licensed under the MIT License.
