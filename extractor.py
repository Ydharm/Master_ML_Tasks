import pytesseract
import cv2
import re
import numpy as np
from PIL import Image

# ✅ Set path to tesseract executable (update if needed)
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

# Label patterns for better matching
label_patterns = {
    "Invoice Number": [r"invoice\s*number", r"invoice\s*no", r"inv\s*#", r"inv\s*no"],
    "Invoice Date": [r"invoice\s*date", r"date\s*of\s*invoice", r"inv\s*date"],
    "Total Amount": [r"total\s*amount", r"total\s*due", r"amount\s*payable", r"total"],
    "Customer Name": [r"billed\s*to", r"bill\s*to", r"customer\s*name", r"to\s*:", r"name\s*:"],
    "Line Items": [r"description", r"product\s*details", r"items", r"item\s*description", r"qty", r"product"]
}

def extract_field(text, patterns):
    for pattern in patterns:
        match = re.search(pattern + r'[:\s\-]*([^\n]+)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""

def extract_invoice_data(image_path):
    try:
        # Read and preprocess image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                          cv2.THRESH_BINARY, 15, 10)

        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(processed)

        # Extract fields using label patterns
        extracted_data = {
            "Invoice Number": extract_field(text, label_patterns["Invoice Number"]),
            "Invoice Date": extract_field(text, label_patterns["Invoice Date"]),
            "Total Amount": extract_field(text, label_patterns["Total Amount"]),
            "Customer Name": extract_field(text, label_patterns["Customer Name"]),
            "Line Items": extract_field(text, label_patterns["Line Items"]),
            "Full Text": text.strip()
        }

        return extracted_data

    except Exception as e:
        return {"Error": f"Extraction Error: {str(e)}"}
