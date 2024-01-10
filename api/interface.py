import os
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from model.predict import predict
import io
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="data/awsIcons_processed"), name="static")

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

    directory = f"data/awsIcons_processed/{predicted_class}"
    if not os.path.exists(directory):
        return {"class": predicted_class, "probability": probability, "image_url": None}

    files = os.listdir(directory)
    print(files)
    if not files:
        return {"class": predicted_class, "probability": probability, "image_url": None}

    selected_file = sorted(files)[-1]
    image_url = f"/static/{predicted_class}/{selected_file}"
    return {"class": predicted_class, "probability": probability, "image_url": image_url}