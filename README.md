# doc-ocr-api
 Inference API for document OCR using EasyOCR and UtrNet
 
 Follow the steps below to get started with this project:

## Using This Repository

### Installation
1. Clone the repository
```
git clone https://github.com/AI-TEAM-R-D-Models/doc-ocr-api.git
```

2. Environment
```
conda create -n document_ocr python=3.11
conda activate document_ocr
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```
# Downloads
## Trained Models

1. [UrduOCR-Large](https://csciitd-my.sharepoint.com/:u:/g/personal/ch7190150_iitd_ac_in/EeUZUQsvd3BIsPfqFYvPFcUBnxq9pDl-LZrNryIxtyE6Hw?e=MLccZi)
2. [UrduOCR-Small](https://csciitd-my.sharepoint.com/:u:/g/personal/ch7190150_iitd_ac_in/EdjltTzAuvdEu-bjUE65yN0BNgCm2grQKWDjbyF0amBcaw?e=yiHcrA)

### Running the Application
To run the application, you can use the following command in your terminal from the root directory of the cloned repo:
```
cd Urdu_OCR
uvicorn API:app --host 0.0.0.0 --port 2005
