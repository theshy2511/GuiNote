import numpy as np
from PIL import Image, ImageFilter
import cv2
from tensorflow.keras.models import load_model
import io

CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MODEL_PATH = "captcha_model.h5"

# Load model chỉ 1 lần
model = load_model(MODEL_PATH)

def preprocess_image(pil_img):
    # 1. Chuyển ảnh sang xám
    img = pil_img.convert("L")

    # 2. Lọc nhiễu bằng median filter
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # 3. Nhị phân hóa (binarize)
    img = img.point(lambda x: 0 if x < 150 else 255, '1')

    # 4. Chuyển sang numpy (OpenCV)
    img_np = np.array(img).astype(np.uint8)

    # 5. Xóa nhiễu nhỏ bằng contour (loại bỏ các vùng < 10 pixel)
    contours, _ = cv2.findContours(img_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < 10:
            cv2.drawContours(img_np, [cnt], 0, 255, -1)

    # 6. Resize đúng size model yêu cầu (100x30 chẳng hạn)
    img_resized = cv2.resize(img_np, (100, 30))  # nhớ: width x height

    # 7. Chuẩn hóa
    img_normalized = img_resized.astype("float32") / 255.0
    img_final = img_normalized.reshape(1, 30, 100, 1)

    return img_final

def decode_prediction(preds):
    return ''.join(CHARACTERS[np.argmax(p)] for p in preds)

def solve_captcha_from_bytes(img_bytes):
    pil_img = Image.open(img_bytes)
    img_input = preprocess_image(pil_img)
    preds = model.predict(img_input)
    return decode_prediction(preds)
