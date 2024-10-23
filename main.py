import os
import PyPDF2
import pdfplumber
import shutil
import fitz
from Extension_Converter import make_pdf
from config import *
from easy_ocr import process_image
from utils import *
temp_paths=create_temp_folders(BASE_FOLDER , SUBFOLDERS)

ocr_results_dict = {}

def extract_text_with_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        tables = []
        for page in pdf.pages:
            text += page.extract_text()
            tables += page.extract_tables()
            
    result_dict = {
        'text': text,
        'tables': {}
    }

    non_empty_tables = [table for table in tables if any(any(cell is not None and cell != '' for cell in row) for row in table)]

    for i, table in enumerate(non_empty_tables, start=1):
        table_key = f"Table{i}"
        result_dict['tables'][table_key] = table

    return result_dict
def extract_images_from_pdf(pdf_path, output_folder):
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    file_folder = os.path.join(output_folder, base_filename)
    os.makedirs(file_folder, exist_ok=True)

    images_list = []

    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]

        # Get images from the page
        images = page.get_images(full=True)

        # Iterate through each image on the page
        for img_index, img_info in enumerate(images):
            image_index = img_info[0]
            base_image = pdf_document.extract_image(image_index)
            image_bytes = base_image["image"]

            # Generate a unique filename for each image
            image_filename = f"image_page_{page_number + 1}_{img_index + 1}.png"
            image_path = os.path.join(file_folder, image_filename)
            images_list.append(image_path)

            # Save the image to the specified folder
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

    # Close the PDF document
    pdf_document.close()

    return images_list, file_folder
# def extract_images_from_pdf(pdf_path, output_folder):
#     base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
#     file_folder=os.path.join(output_folder,base_filename)
#     os.makedirs(file_folder, exist_ok=True)
#     # print(base_filename)
#     images_list=[]
#     with open(pdf_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         for page_num in range(len(pdf_reader.pages)):
#             page = pdf_reader.pages[page_num]

#             for img_num, image in enumerate(page.images):
#                 # Generate a unique filename for each image
#                 image_filename = f"image_{page_num + 1}_{img_num + 1}.png"
#                 image_path = os.path.join(output_folder,base_filename, image_filename)
#                 images_list.append(image_path)
#                 with open(image_path, 'wb') as f:
#                     f.write(image.data)
#     return images_list,file_folder
# def image_ocr(output_folder):
#     # Check if the output_folder is empty
#     if not os.listdir(output_folder):
#         print(f"The folder {output_folder} is empty.")
#     else:
#         # Initialize the OCR reader  # this needs to run only once to load the model into memory
#         ocr_results_dict = {}
#         # Loop through all files in the output_folder
#         for filename in os.listdir(output_folder):
#             if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Add more image extensions if needed
#                 image_path = os.path.join(output_folder, filename)
#                 result = reader.readtext(image_path, detail=0)
#                 if result:
#                     key = f"{os.path.splitext(filename)[0]}"
#                     ocr_results_dict[key] = result
#         return ocr_results_dict


def process_pdf(file_path, output_folder=temp_paths['temp_pdf']):
    # text and table data
    results = extract_text_with_pdfplumber(file_path)
    # print(results)
    # images save 
    images_list,file_folder=extract_images_from_pdf(file_path, output_folder)
    images_data = {}
    for filename in images_list:
        # print(filename)
        pdf_image_result = process_image(filename)
        key = os.path.splitext(os.path.basename(filename))[0]
        images_data[key] = pdf_image_result
        
    
    results['images'] = images_data
    shutil.rmtree(file_folder, ignore_errors=True)
    return results

def main(file_path):
# Main code
    # file_path = 'test1.pdf'
    file_extension = file_path.lower().split('.')[-1]
    # print("file extension:",file_extension)
    if file_extension == 'pdf':
        results=process_pdf(file_path=file_path)
        return results
    elif file_extension in IMAGES_TYPE:
        result=process_image(file_path)
        results = {'text': '', 'tables': {}, 'images': {'image1': result}}
        # print(results)
        return results
    elif file_extension=="txt":
        result=read_text_file(file_path)
        results = {'text': result, 'tables': {}, 'images': {'image1': ""}}
        # print(results)
        return results
    elif file_extension in NOT_SUPPORTED_FORMAT:
        return "This format is not supported!"
        
    else:
        # Unsupported file type, try to convert to PDF
        file_folder=os.path.splitext(os.path.basename(file_path))[0]
        file_folder=os.path.join(BASE_FOLDER,"convert",file_folder)
        
        file_path=make_pdf(file_path,file_extension,file_folder)
        results=process_pdf(file_path=file_path)
        # shutil.rmtree(file_folder, ignore_errors=True)
        return results

# if __name__ == "__main__":
#     # Test cases
#     file_paths = [
#         os.path.join("TestSample", "GrouperTest", "18-47-03-312.jpg"),
#         os.path.join("TestSample", "test1.pdf"),
#         os.path.join("TestSample", "test1.docx"),
#         os.path.join("TestSample", "test2.docx"),
#         os.path.join("TestSample", "file-sample_1MB.doc"),
#         # os.path.join("TestSample", "annual-enterprise-survey-2021-financial-year-provisional-csv.csv"),
#         os.path.join("TestSample", "testxlx.xlsx"),
        
#         os.path.join("TestSample", "Dickinson_Sample_Slides.pptx")
#     ]

#     # Process each file path
#     for file_path in file_paths:
#         print(main(file_path=file_path))