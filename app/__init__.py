from flask import Flask
from ultralytics import YOLO

def create_app():
    app = Flask(__name__)
    from .api import ocr_bp
    app.register_blueprint(ocr_bp)

    with app.app_context():
        # Load model once
        app.models = {
            'adhaarModel': YOLO('models/aadhaarYolov8.pt'),
            'panModel': YOLO('models/PanModal_v3.pt')  # Load additional models as needed
        }

    return app
