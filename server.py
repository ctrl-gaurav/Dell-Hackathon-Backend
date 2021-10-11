from fastapi import FastAPI, Request, UploadFile
from fastapi.params import File
from fastapi.datastructures import UploadFile
from fastapi.templating import Jinja2Templates 
from starlette.requests import Request
import shutil
import os
import ocr
import requests


app = FastAPI()

templates = Jinja2Templates(directory='templates')

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/upload')
def perform_ocr(file: UploadFile = File(...)):
    temp_file = _save_file_to_disk(file, path="temp", save_as="temp_file")
    text = ocr.pdfToTxt(temp_file)
    return {"filename": file.filename, "text": text}
    



def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file
