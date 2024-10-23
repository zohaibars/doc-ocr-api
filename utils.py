import os
import socket
from langdetect import detect_langs
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def create_temp_folders(base_folder, subfolders):
    """
    Create temporary folders within a base folder.

    Parameters:
    - base_folder (str): Path to the base folder.
    - subfolders (list): A list of subfolders to be created within the base folder.
    """
    # Create the base folder if it doesn't exist
    os.makedirs(base_folder, exist_ok=True)
    temp_paths={}
    # Create temporary folders within the base folder
    for subfolder in subfolders:
        subfolder_path = os.path.join(base_folder, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)
        temp_paths[subfolder]=subfolder_path
    return temp_paths



def get_ip_address():
    try:
        # Get the hostname of the local machine
        host_name = socket.gethostname()
        
        # Get the IP address of the local machine
        ip_address = socket.gethostbyname(host_name)
        
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None
# from nltk.corpus import words
# import nltk
# nltk.download('words')

# def is_english_word(word):
#     # Check if the word is in the English dictionary
#     return word.lower() in words.words()
def separate_urdu_english(result):
    # Initialize variables to store English and Urdu text
    english_text = ""
    urdu_text = ""
    modified_result = []
    # text_only = [item[1] for item in result]
    # for text_info in result:
    for item in result:
        text = item[1]
        urdu_found=False
        # print("word:",text)
        try:
            # Check if the text is not empty or too short
            if text:
                # Detect language and append to the respective string
                # language=detect(text)
                detected_languages = detect_langs(text)
                # print("word:",text,"language:",language)
                for lang in detected_languages:
                    # print(f"word :{text},Language: {lang.lang}, Probability: {lang.prob}")
                    if lang.lang=='ur' or lang.lang=='fa':
                        urdu_found=True
                        break
                    else:
                        urdu_found=False
                if urdu_found:
                    urdu_text += text + " "
                else:
                    # if is_english_word(text):
                    english_text += text + " "
                    continue
            modified_result.append(item)
        except LangDetectException as e:
            # print("no lang info :",text)
            continue 

    return english_text.strip(), urdu_text.strip(),modified_result
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"