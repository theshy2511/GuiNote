import os
import pandas as pd
import time

# ==== CẤU HÌNH ====
IMAGE_FOLDER = "captchas"
CSV_FILE = "labels.csv"
START_INDEX = 30

# ==== ĐỌC DANH SÁCH ẢNH ====
image_files = sorted(f for f in os.listdir(IMAGE_FOLDER) if f.endswith(".png"))
image_files = [f for f in image_files if int(f.split(".")[0]) >= START_INDEX]

# ==== ĐỌC FILE CSV NẾU CÓ ====
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    labeled_files = set(df["filename"])
else:
    df = pd.DataFrame(columns=["filename", "label"])
    labeled_files = set()

# ==== LỌC ẢNH CHƯA GÁN NHÃN ====
image_files = [f for f in image_files if f not in labeled_files]

print(f"📸 Số ảnh chưa gán nhãn: {len(image_files)}")

# ==== GÁN NHÃN ====
for filename in image_files:
    full_path = os.path.join(IMAGE_FOLDER, filename)
    os.startfile(full_path)  # mở bằng app ảnh mặc định

    # Cho người dùng xem ảnh 1-2 giây trước khi nhập
    time.sleep(1)

    label = input(f"🔤 Nhập CAPTCHA cho {filename}: ").strip().upper()

    # Ghi vào CSV
    df = pd.concat([df, pd.DataFrame([[filename, label]], columns=["filename", "label"])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    print(f"✅ Đã lưu: {filename} → {label}")

print("\n🎉 Hoàn tất gán nhãn!")
