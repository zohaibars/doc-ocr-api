import requests
import socket
# sys.path.append('..') 
# Get the hostname of the local machine
host_name = socket.gethostname()
URDU_API_BASE_URL=socket.gethostbyname(host_name)
# Replace with the URL where your FastAPI server is running
Dcoument_base_url = "http://"+URDU_API_BASE_URL+":2006"
Dcoument_handshake_url = "http://"+URDU_API_BASE_URL+":2007"
# Replace with your API key
api_key = "apikey1"
def handshake_status():
    return requests.get(f"{Dcoument_handshake_url}/handshake/")
def Document_OCR(file_path):
    try:
        # print('API IS LIVE')
        with open(file_path, 'rb') as file_path_:
            files = {'file': file_path_}
            headers={
                'api_key': api_key
            }
            response = requests.post(f"{Dcoument_base_url}/ocr/", files=files, headers=headers)
       
        if response.status_code == 200:
            result = response.json()
            print(result)
        else:
            print("Error:", response.text)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
#     english = r"TestSample/Comparing-our-proposed-method-with-the-state-of-the-art-frameworks-on-colorectal-tissue.png"
#     Document_OCR(english)
#     urdu=r"TestSample\GrouperTest\18-47-03-312.jpg"
#     Document_OCR(urdu)
    if handshake_status():

        urdu=r"TestSample/UrduOCR Test/chunk_First_4.png"
        Document_OCR(urdu)
    else :
        print("API not live")
    # urdu=r"D:\b.ts"
    # Document_OCR(urdu)