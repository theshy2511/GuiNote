from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import string

CHARACTERS = string.ascii_uppercase + string.digits

def decode_prediction(preds):
    return ''.join([CHARACTERS[np.argmax(p)] for p in preds])

def predict_image(image_path):
    img = Image.open(image_path).convert("L").resize((100, 30))
    img = np.array(img) / 255.0
    img = img.reshape((1, 30, 100, 1))

    model = load_model("captcha_model.h5")
    preds = model.predict(img)
    return decode_prediction(preds)

# Ví dụ dùng thử
print("Đoán CAPTCHA:", predict_image("captchas/1.png"))
