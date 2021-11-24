from os import name
import tensorflow as tf
import numpy as np
from numpy import ndarray, array, expand_dims, argmax
from PIL import Image
import io


MODELS_DIR = '../saved_models/{}'
IMAGE_SIZE = 64
PREDICTED_IMAGES_DIR = './predicted_images/{}.png'

class_names = [
    'Bacterial spot',
    'Early blight',
    'Late blight',
    'Leaf Mold',
    'Septoria leaf spot',
    'Spider mites Two-spotted spider mite',
    'Target Spot',
    'Yellow Leaf Curl Virus',
    'mosaic virus',
    'healthy'
]

class Prediction:
    def __init__(self, class_:int, confidance:float) -> None:
        self.class_ = class_
        self.confidance = confidance

    @property
    def class_name(self)->str:
        return class_names[self.class_]

    def response(self) -> dict:
        response = {
            'class': self.class_name,
            'confidance': float(self.confidance)
        }
        return response


def load_model(model_version:str) -> tf.keras.models.Model:
    model_name = MODELS_DIR.format(model_version)
    model = tf.keras.models.load_model(model_name)

    return model

# convert raw file data into numpy.ndarray
def convert_raw_to_ndarray(raw_data: bytes) -> ndarray:
        io_file = io.BytesIO(raw_data)
        pil_image = Image.open(io_file)
        pil_image  = pil_image.resize((IMAGE_SIZE, IMAGE_SIZE))
    
        return array(pil_image)


def predict_image(img_array: ndarray) -> Prediction:
    model = load_model(2)

    predicted = model.predict(expand_dims(img_array, 0))
    confidance = np.max(predicted)
    predicted_class = argmax(predicted, axis=1)[0]

    prediction = Prediction(predicted_class, confidance)

    return prediction

def save_predicted_image(name: str, image: Image):
    image.save(PREDICTED_IMAGES_DIR.format(name))