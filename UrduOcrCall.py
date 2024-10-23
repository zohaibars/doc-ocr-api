import requests
import socket
from config import URDU_API_BASE_URL,API_KEY
# Replace with the URL where your FastAPI server is running
base_url = "http://"+URDU_API_BASE_URL+":2005"
def Urdu_OCR(file_path):
    try:
        with open(file_path, 'rb') as file_path_:
            files = {'file': file_path_}
            headers={
                'api_key': API_KEY
            }
            # headers = {'api_key': api_key,'purpose':"report"}  # Include the API key in the header
            response = requests.post(f"{base_url}/urdu_ocr/", files=files, headers=headers)

        if response.status_code == 200:
            result = response.json()
            # print(result)
            return result
           
    
        else:
            return ("Error:", response.text)
    except Exception as e:
        return ("Error:", str(e))

# if __name__ == "__main__":
#     video_path = r"C:\Users\muham\OneDrive\Desktop\Forbmax Projects\Document-Ocr\TestSample\UrduOCR Test\Geonews000a41e5-369e-4f8b-9af3-6bb73c36a167.jpg"
#     OCR_image(video_path)
