from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from secrets import token_hex
from time import time
from io import BytesIO
from utils import convert_raw_to_ndarray, predict_image, save_predicted_image

import schemas, models, crud
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/predict')
async def predict(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    start_time = time()

    img_data = await file.read()
    img_array = convert_raw_to_ndarray(img_data)
    prediction = predict_image(img_array)

    db_prediction = crud.create_prediction(db, prediction.class_name, 
                    prediction.confidance, time()-start_time)

    save_predicted_image(db_prediction.image_name, Image.open(BytesIO(img_data)))

    return {
        'class': db_prediction.class_name,
        'confidance': db_prediction.confidance,
    }
