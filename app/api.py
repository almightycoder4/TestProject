from flask import Blueprint
import requests
import os
from .routes.adhaarApi import ocrAdhaar
from .routes.panApi import ocrPan
ocr_bp = Blueprint('ocr', __name__)
session = requests.Session()
mode = os.getenv("PROJECT_MODE")

@ocr_bp.route('/ocrPan', methods=['POST'])
def getResponse_Pan():
    return ocrPan(mode, session)

@ocr_bp.route('/ocrAdhaar', methods=['POST'])
def getResponse_Adhaar():
    return ocrAdhaar(mode, session)