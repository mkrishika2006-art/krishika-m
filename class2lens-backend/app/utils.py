import os
from PIL import Image
from io import BytesIO

UPLOAD_FOLDER = "uploads"

def save_uploaded_image(file, filename):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    img = Image.open(BytesIO(file))
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img.save(filepath)
    return filepath
