from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(f"Image size must be 70x70 or less - size of image is {img.size}")


def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = [".jpg", ".png", ".jpeg", ".gif"]
    if not ext.lower() in valid_extension:
        raise ValidationError("Unsupported file extension. You can only upload jpg, png, jpeg, gif files.")
