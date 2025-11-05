import os
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
import string

# Cấu hình
CHARACTERS = string.ascii_uppercase + string.digits  # A-Z + 0-9
CHAR_TO_LABEL = {char: idx for idx, char in enumerate(CHARACTERS)}
MAX_LEN = 4  # CAPTCHA có 4 ký tự

# Đọc dữ liệu nhãn
df = pd.read_csv("labels.csv")
data = []
labels = []

def encode_label(text):
    return [CHAR_TO_LABEL[c] for c in text]

for _, row in df.iterrows():
    path = os.path.join("captchas", row['filename'])
    img = Image.open(path).convert("L").resize((100, 30))  # grayscale, chuẩn hóa kích thước
    img = np.array(img) / 255.0
    data.append(img)
    labels.append(encode_label(row['label']))

data = np.array(data).reshape(-1, 30, 100, 1)
labels = np.array(labels)

# Tách tập train/test
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Xây dựng mô hình CNN
def build_model():
    input_layer = layers.Input(shape=(30, 100, 1))
    x = layers.Conv2D(32, (3,3), activation='relu')(input_layer)
    x = layers.MaxPooling2D((2,2))(x)
    x = layers.Conv2D(64, (3,3), activation='relu')(x)
    x = layers.MaxPooling2D((2,2))(x)
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)

    outputs = []
    for _ in range(MAX_LEN):
        outputs.append(layers.Dense(len(CHARACTERS), activation='softmax')(x))

    model = models.Model(inputs=input_layer, outputs=outputs)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'] * MAX_LEN)
    return model

model = build_model()

# Huấn luyện mô hình
model.fit(X_train, [y_train[:, i] for i in range(MAX_LEN)],
          validation_data=(X_test, [y_test[:, i] for i in range(MAX_LEN)]),
          epochs=20, batch_size=8)

# Lưu mô hình
model.save("captcha_model.h5")
print("✅ Đã huấn luyện xong và lưu mô hình vào captcha_model.h5")
