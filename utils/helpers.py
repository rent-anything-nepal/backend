import re
import pytesseract
from PIL import Image, ImageFilter

from rest_framework.exceptions import ValidationError


def check_if_object_id_exists(self):
    if not self.content_type.model_class().objects.filter(id=self.object_id).exists():
        raise ValidationError({"object_id": ["Does not exist"]})


def scan_image_for_text(path):
    image = Image.open(path)
    resized_image = image.resize((1200, 800))
    # Convert to grayscale
    grayscale_image = resized_image.convert("L")
    # Use a median filter to remove noise
    bilateral_filter_image = grayscale_image.filter(ImageFilter.MedianFilter(size=3))
    # Extract text
    return pytesseract.image_to_string(bilateral_filter_image)


def validate_presence_of_nepal_government_text(scanned_text):
    govt_of_nepal = "Government of Nepal"
    if govt_of_nepal in scanned_text:
        return True
    return False


def get_citizenship_number(scanned_text):
    id_regex = r"Citizenship\sCertificate\sNo\.:\s(?P<id>(?:\d+-){2,3}\d+)"
    match = re.search(id_regex, scanned_text)
    if match:
        return match.group("id")
    raise ValueError("Citizenship number not found inside the scanned text")


def get_full_name(scanned_text):
    full_name_regex = r"Full\sName:\s(?P<full_name>[A-Z]+\s[A-Z]+(\s[A-Z]+)?)"
    match = re.search(full_name_regex, scanned_text)
    if match:
        return match.group("full_name")
    raise ValueError("Full name not found inside the scanned text")
