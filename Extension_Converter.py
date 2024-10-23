from File_Converter import *
from config import *
def make_pdf(file_path,extension,output_folder):

    if extension=="doc":
        print("conveting doc to pdf")
        docx=doc_to_pdf(file_path,output_folder)
        # print(docx)
        # pdf=docx_to_pdf(docx)
        return docx
    elif extension in EXCEL_SUPPORTED_FORMATS:
        print("conveting excel to pdf",file_path)
        
        return excel_to_pdf(file_path,output_folder)
    elif extension in DOC_SUPPORTED_FORMATS:
        print("converting docx into pdf")
        return convert_to_pdf(file_path,output_folder)

    elif extension in POWERPOINT_SUPPORTED_EXTENSIONS:
        print("conveting excel to pdf")
        return ppt_to_pdf(file_path,output_folder)
    else:
        print("converting other formats ")
        return libreoffice_convert_to_pdf(file_path,output_folder)
# if __name__ == "__main__":
#     # Test cases
#     # print(make_pdf(os.path.join("TestSample", "test1.docx"),'docx',"temp"))
#     file_paths = [
#         os.path.join("TestSample", "annual-enterprise-survey-2021-financial-year-provisional-csv.csv"),
#         # os.path.join("TestSample", "Dickinson_Sample_Slides.pptx"),
#         # os.path.join("TestSample", "Dickinson_Template_red.pptx"),
#         # os.path.join("TestSample", "GrouperTest", "18-47-03-312.jpg"),
#         # os.path.join("TestSample", "file-sample_1MB.doc"),
#         # os.path.join("TestSample", "test1.pdf"),
#         # os.path.join("TestSample", "test1.docx"),
#         os.path.join("TestSample", "test2.docx"),
#         os.path.join("TestSample", "file-sample_1MB.doc")
#     ]

#     # Process each file path
#     for file_path in file_paths:
#             # file_path = 'test1.pdf'
#         file_extension = file_path.lower().split('.')[-1]
#         print("file extension:",file_extension)
#         file_folder=os.path.splitext(os.path.basename(file_path))[0]
#         file_folder=os.path.join(BASE_FOLDER,"convert",file_folder)
    
#         print(make_pdf(file_path,file_extension,file_folder))