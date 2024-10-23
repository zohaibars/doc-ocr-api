import os
import subprocess
import pypandoc
def doc_to_pdf(input_file, output_dir=os.path.join('temp', 'convert')):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.pdf')

        if input_file.lower().endswith('.docx'):
            # Use Pandoc to convert DOCX to PDF
            subprocess.run(['pandoc', '--from=docx', input_file, '-o', output_pdf_file])
        elif input_file.lower().endswith('.doc'):
            # Use libreoffice to convert DOC to PDF
            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_file])
        else:
            return "Error: Unsupported file format."

        return output_pdf_file
    except Exception as e:
        return f"Error converting document to PDF: {str(e)}"

def convert_to_pdf(input_file, output_dir=os.path.join('temp', 'convert')):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.pdf')

        # Use pypandoc to convert DOCX/DOC to PDF
        pypandoc.convert_file(input_file, 'pdf', outputfile=output_pdf_file, extra_args=['--pdf-engine=xelatex'])

        return output_pdf_file
    except Exception as e:
        return f"Error converting document to PDF: {str(e)}"
    

def excel_to_pdf(input_file, output_dir=os.path.join('temp', 'convert')):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.pdf')
        # Use libreoffice to convert Excel formats to PDF
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_file])
        return output_pdf_file
     

    except Exception as e:
        return f"Error converting Excel document to PDF: {str(e)}"
def ppt_to_pdf(input_file, output_dir=os.path.join('temp', 'convert')):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.pdf')

        # Use unoconv for PowerPoint to PDF conversion
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_file])

        return output_pdf_file

    except Exception as e:
        return f"Error converting PowerPoint document to PDF: {str(e)}"
    
def libreoffice_convert_to_pdf(input_file, output_dir=os.path.join('temp', 'convert')):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.pdf')

        # Use unoconv for PowerPoint to PDF conversion
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_file])

        return output_pdf_file

    except Exception as e:
        return "Error converting document to PDF"
# Test your functions
# print(convert_to_pdf(os.path.join("TestSample", "test1.docx")))
# print(convert_to_pdf(os.path.join("TestSample", "test2.docx")))
# print(doc_to_pdf(os.path.join("TestSample", "file-sample_1MB.doc")))
# print(ppt_to_pdf(os.path.join("TestSample", "Dickinson_Sample_Slides.pptx")))
