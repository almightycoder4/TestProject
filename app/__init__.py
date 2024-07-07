from flask import Flask
from ultralytics import YOLO

def create_app():
    app = Flask(__name__)
    from .api import ocr_bp
    app.register_blueprint(ocr_bp)

    with app.app_context():
        # Load model once
        app.model = YOLO('models/aadhaarYolov8.pt')

    return app
