from fastapi import FastAPI, File, UploadFile
from model.predict import predict

import io
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    image_stream = io.BytesIO(contents)
    image_stream.seek(0)

    image = Image.open(image_stream)
    predicted_class, probability = predict(image)
    return {"class": predicted_class, "probability": probability}