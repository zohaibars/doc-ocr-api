::start cmd /k "uvicorn STT.API.app:app --host 0.0.0.0 --port 2000 --reload"
start cmd /k "uvicorn Urdu_OCR.API:app --host 0.0.0.0 --port 2000 "