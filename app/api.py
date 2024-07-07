import re
from flask import Blueprint, request, jsonify, current_app
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import base64
import requests
from .services.adhaarServices.ocr import process_results
import os
import io
from .routes.adhaarApi import ocrAdhaar
ocr_bp = Blueprint('ocr', __name__)
session = requests.Session()
mode = os.getenv("PROJECT_MODE")

@ocr_bp.route('/ocrPan', methods=['POST'])
def ocr_pan():
    try:
        print("API HIT ************* OCRPAN")
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request payload"}), 400

        if mode == "prod":
            if not data.get('image'):
                return jsonify({"error": "Image data/buffer is required"}), 400

            # Removing 'data:image/png;base64,' from buffer
            imgBuffer = data.get('image')
            imgBuffer = re.sub("^data:image/.+;base64,", "", imgBuffer)
            # Adjust base64 string padding
            if len(imgBuffer) % 4:
                imgBuffer += '=' * (4 - len(imgBuffer) % 4)
                
            try:
                img_data = base64.b64decode(imgBuffer)
                img = Image.open(BytesIO(img_data))
                img.verify()  # Verify image format
                img = Image.open(io.BytesIO(img_data))  # Re-open image after verification
            except (base64.binascii.Error, ValueError) as decode_err:
                return jsonify({"error": f"Image decoding failed: {str(decode_err)}"}), 400
            except UnidentifiedImageError:
                return jsonify({"error": "Unable to identify image format."}), 400

        elif mode == "dev":
            if not data.get('imgUrl'):
                return jsonify({"error": "Image URL is required"}), 400

            img_url = data.get('imgUrl')
            response = session.get(img_url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.verify()  # Verify image format
            img = Image.open(BytesIO(response.content))  # Re-open image after verification

        else:
            return jsonify({"error": "Invalid mode configuration"}), 500

        # Check image format
        if img.format not in ['JPEG', 'JPG', 'PNG']:
            return jsonify({"error": "Invalid image format. Only JPG and PNG are supported."}), 400

        # Run detection
        model = current_app.model
        results = model.predict(source=img, save=False)
        extracted_data = process_results(results, img)
        
        if extracted_data.get('statusCode') == 400:
            return jsonify(extracted_data), 400
        
        return jsonify(extracted_data), 200
    except requests.RequestException as req_err:
        return jsonify({"error": f"Image download failed: {str(req_err)}"}), 500
    except UnidentifiedImageError:
        return jsonify({"error": "Unable to identify image format."}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@ocr_bp.route('/ocrAdhaar', methods=['POST'])
def getResponse():
    return ocrAdhaar(mode, session)