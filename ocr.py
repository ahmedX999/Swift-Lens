import cv2
import pytesseract
import re

# Path to Tesseract executable (adjust based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_from_image(image_path, custom_data_path=None):
    """
    Extracts specific information from an image of a Moroccan ID card.

    Args:
        image_path: Path to the image file.
        custom_data_path: Path to a directory containing custom Tesseract training data (optional).

    Returns:
        A dictionary containing extracted information (name, last name, date of birth, ID number).
    """

    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image (adjust based on your requirements)
    # ... (e.g., noise reduction, binarization)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply preprocessing (adjust based on your requirements)
    # ... (e.g., adaptive thresholding, skew correction)

    # Run Tesseract OCR on the preprocessed image
    if custom_data_path:
        extracted_text = pytesseract.image_to_string(gray_image, config='--psm 6 -c lang=mor')
        
    else:
        extracted_text = pytesseract.image_to_string(gray_image)
       

    # Extract specific information using regular expressions
    name_match = re.findall(r"([A-Z]+)", extracted_text) 
    date_of_birth_match = re.findall(r"\d{2}.\d{2}.\d{4}", extracted_text)
    id_number_match = re.findall(r"[A-Z]+\d{1,8}", extracted_text)
    

    # Check if any matches were found
    if name_match and date_of_birth_match and id_number_match:
        # Store extracted information in a dictionary
        extracted_data = {
            "name": " ".join(name_match[11]+" "+name_match[12]),  # assume first match is full name
            "date_of_birth": date_of_birth_match[0],
            "id_number": id_number_match[0],
       
        }
        return extracted_data
    else:
        # Handle the case where no matches were found
        return {"error": "No matches found in the OCR results."}

if __name__ == "__main__":
    # Provide the path to the image you want to process
    image_path = 'photos/id001.jpg'

    # Optionally specify a custom data path for Tesseract
    # custom_data_path = '/path/to/moroccan_id_data'

    # Perform OCR on the image and extract specific information
    extracted_data = ocr_from_image(image_path)

    # Display the extracted information
    if "error" in extracted_data:
        print("Error:", extracted_data["error"])
    else:
        print("Extracted Information:")
        print(f"Name: {extracted_data['name']}")
        print(f"Date of Birth: {extracted_data['date_of_birth']}")
        print(f"ID Number: {extracted_data['id_number']}")
        
        
