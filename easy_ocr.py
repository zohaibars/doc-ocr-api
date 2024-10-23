import os
import cv2
from ocr_initializer import initialize_ocr_reader
from UrduOcrCall import Urdu_OCR
import shutil
from config import *
from utils import separate_urdu_english
import re
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import torch

def remove_special_characters_regex(input_string):
    pattern = r'[^a-zA-Z0-9\s]'
    clean_string = re.sub(pattern, '', input_string)
    return clean_string


torch.cuda.empty_cache()
# Initialize OCR reader
reader = initialize_ocr_reader()

# Function to sort bounding boxes from top-right to bottom-left
def sort_boxes(bounds):
    sorted_bounds = sorted(bounds, key=lambda b: (-b[0][0][1], -b[0][0][0]))
    return sorted_bounds

# Convert PIL image to a NumPy array
def pil_to_cv2(img):
    return np.array(img)

# Define function to crop the image based on bounding box coordinates
def crop_image(img, bbox):
    (tl, tr, br, bl) = bbox  # top-left, top-right, bottom-right, bottom-left
    left = min(tl[0], bl[0])
    top = min(tl[1], tr[1])
    right = max(tr[0], br[0])
    bottom = max(bl[1], br[1])
    cropped_img = img.crop((left, top, right, bottom))
    return cropped_img

# Define function to process the image
def process_image(input_image, reader=reader):
    # Check if the file exists
    if not os.path.exists(input_image):
        return f"File not found: {input_image}"

    # Open the image using PIL
    img_pil = Image.open(input_image)
    if img_pil is None:
        return f"Failed to read the image: {input_image}"

    # Convert the PIL image to a NumPy array
    img_np = pil_to_cv2(img_pil)

    # OCR the image (pass the NumPy array to EasyOCR)
    result = reader.readtext(img_np)
    final_text = ""
    if result:
        english_text, urdu_text, result = separate_urdu_english(result)
        english_text = remove_special_characters_regex(english_text)
        if english_text:
            final_text += english_text
        if urdu_text:
            image_name = os.path.basename(input_image)
            urdu_text = ""

            # Sort the bounding boxes in top-right to bottom-left order
            sorted_result = sort_boxes(result)

            # Create a directory for cropped images
            directory = os.path.join(BASE_FOLDER, CROPS)
            os.makedirs(directory, exist_ok=True)

            # Loop over the sorted bounding boxes and crop the image
            for i, (bbox, text, confidence) in enumerate(reversed(sorted_result)):
                cropped_img = crop_image(img_pil, bbox)  # Crop the image based on the bounding box

                # Save the cropped image in sorted order
                crop_image_path = os.path.join(directory, f"image_{i+1}.png")
                cropped_img.save(crop_image_path)

                try:
                    urdu_text += " " + Urdu_OCR(crop_image_path)
                    # print("urdu_text \n\n", urdu_text)
                except:
                    return "Urdu OCR API not live, check it!!!!"
            shutil.rmtree(directory, ignore_errors=True)
        final_text += urdu_text

        return final_text

# Example usage
# file_path = "/home/zohaib/Downloads/1.png"  # Update with your image path
# print(process_image(file_path))










#############################################################
#############################################################
#################### Previous Code ##########################
#############################################################

# import os
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
# import cv2
# from ocr_initializer import initialize_ocr_reader
# from UrduOcrCall import Urdu_OCR
# import shutil
# from config import *
# from utils import separate_urdu_english
# import re

# def remove_special_characters_regex(input_string):
#     # Define regex pattern to match special characters
#     pattern = r'[^a-zA-Z0-9\s]'
#     # Use regex sub() function to replace special characters with an empty string
#     clean_string = re.sub(pattern, '', input_string)
#     return clean_string

# reader=initialize_ocr_reader()


# def process_image(input_image,reader=reader):
    
#     img= cv2.imread(input_image)
#     result = reader.readtext(img, detail=1, paragraph=False)
#     final_text=""
#     if result:
#         english_text, urdu_text,result = separate_urdu_english(result)
#         english_text=remove_special_characters_regex(english_text)
#         if english_text:
#             final_text += english_text
#         if urdu_text:
#             image_name=os.path.basename(input_image)
#             temp_name=0
#             urdu_text=""
#             directory=os.path.join(BASE_FOLDER,CROPS,image_name)
#             os.makedirs(directory, exist_ok=True)
#             for i, (bbox, _, _) in enumerate(result):
#                 (tl, tr, br, bl) = bbox
#                 tl = (int(tl[0]), int(tl[1]))
#                 br = (int(br[0]), int(br[1]))
#                 crop_object =img[tl[1]:br[1], tl[0]:br[0]]
#                 print("tl \n\n ", tl, "br \n\n", br)
#                 store_image_path=os.path.join(directory,str(temp_name)+".png")
#                 cv2.imwrite(store_image_path, crop_object)
#                 temp_name=temp_name+1
#                 try:
#                     urdu_text += " " + Urdu_OCR(store_image_path)
#                     print("urdu_text \n\n", urdu_text)
#                 except:
#                     return "Urdu OCR API not live, check it!!!!"
#             #shutil.rmtree(directory, ignore_errors=True)
#         final_text +=urdu_text
        
#         return final_text
        