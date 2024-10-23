import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header
import concurrent.futures
import asyncio
from main import read_image as urdu_ocr
app = FastAPI()    
user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}
# Define a directory to store uploaded videos
upload_dir = "urdu_ocr_uploads"
os.makedirs(upload_dir, exist_ok=True)

def process_file(file: UploadFile):
    try:
        # Read the uploaded file into memory
        file_content = file.file.read()

        # Extract the file extension from the original filename
        file_extension = os.path.splitext(file.filename)[1].lower()

        # Generate a unique filename (e.g., using UUID) or use the original filename
        # Here, I'm using the original filename without the extension
        file_name = os.path.splitext(file.filename)[0]

        # Define the path where the file will be saved
        file_path = os.path.join(upload_dir, f"{file_name}{file_extension}")

       
        # Save the file in the specified directory
        with open(file_path, "wb") as temp_file:
            temp_file.write(file_content)
        # Check if the file already exists
        if not os.path.exists(file_path):
            print(f"File not found/{file_path}")
            return {"error": f"File not found/{file_path}"}
        try:
            # Process the file (e.g., perform OCR)
            result = urdu_ocr(image_path=file_path)
            # You can do something with the result here

        except Exception as e:
            return {"error": f"OCR error: {str(e)}"}

        finally:
            # Always try to remove the uploaded file after processing
            try:
                os.remove(file_path)
            except Exception as e:
                return {"error": f"File delete error: {str(e)}"}
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Dependency to validate the API key
async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.post("/urdu_ocr/")
async def urdu_ocr_endpoint(
    file: UploadFile,
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: process_file(file)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2005, reload=True)
    # uvicorn API:app --host 0.0.0.0 --port 2005 --reload

