import requests
import socket
# sys.path.append('..') 
# Get the hostname of the local machine
host_name = socket.gethostname()
URDU_API_BASE_URL=socket.gethostbyname(host_name)
# Replace with the URL where your FastAPI server is running
base_url = "http://"+URDU_API_BASE_URL+":2000"
# Replace with your API key
api_key = "apikey1"
def OCR_image(file_path):
    try:
        with open(file_path, 'rb') as file_path_:
            files = {'file': file_path_}
            headers={
                'api_key': api_key
            }
            # headers = {'api_key': api_key,'purpose':"report"}  # Include the API key in the header
            response = requests.post(f"{base_url}/urdu_ocr/", files=files, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(result)
           
    
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    video_path = r"C:\Users\muham\OneDrive\Desktop\Forbmax Projects\Document-Ocr\TestSample\UrduOCR Test\Geonews000a41e5-369e-4f8b-9af3-6bb73c36a167.jpg"
    OCR_image(video_path)
