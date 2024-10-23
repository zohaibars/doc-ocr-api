import os
import concurrent.futures
import asyncio
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header, Query
from fastapi.responses import JSONResponse
import requests
import socket
host_name = socket.gethostname()
URDU_API_BASE_URL=socket.gethostbyname(host_name)
# Replace with the URL where your FastAPI server is running
base_url = "http://"+URDU_API_BASE_URL+":2006"
# Replace with your API key
api_key = "apikey1"
def check_api_status(base_url):
    try:
        # Use a short timeout, for example, 5 seconds
        response = requests.get(base_url + "/docs", timeout=5)
        
        # Check if the status code is in the range 200-299, indicating a successful request
        if response.ok:
            return True
        else:
            return False

    except requests.RequestException as e:
        return (f"Could not connect to the API at {base_url}. Error: {e}")

app = FastAPI()

user_api_keys = {
    "user1": "apikey1",
}



async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail={"error": "Invalid API key"})
    return api_key

@app.get("/handshake/")
async def handshake_endpoint(

):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: check_api_status(base_url)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2006, reload=True)
    # uvicorn app:app --host 0.0.0.0 --port 2006 --reload