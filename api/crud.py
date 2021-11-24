from secrets import token_hex
from time import time
from sqlalchemy.orm import Session

import models

def create_prediction(db: Session, class_name:str, confidance: float, took: float):

    db_prediction = models.Prediction(
        image_name=str(token_hex(16)),
        class_name=class_name,
        confidance=confidance,
        took=took
    )

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return db_prediction
