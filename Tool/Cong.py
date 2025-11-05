import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ==== CẤU HÌNH ====
SAVE_DIR = "captchas"  # thư mục lưu ảnh
START_INDEX = 86       # bắt đầu từ ảnh số 51
TOTAL = 7             # số lượng ảnh muốn lưu

# Tạo thư mục nếu chưa có
os.makedirs(SAVE_DIR, exist_ok=True)

# ==== KHỞI TẠO SELENIUM ====
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # không hiển thị trình duyệt
options.add_argument("--window-size=1200,800")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# ==== TẢI ẢNH CAPTCHA ====
for i in range(START_INDEX, START_INDEX + TOTAL):
    driver.get("https://sinhvien.huit.edu.vn/tra-cuu-thong-tin.html")
    try:
        captcha_img = wait.until(EC.presence_of_element_located((By.ID, "newcaptcha")))
        src = captcha_img.get_attribute("src")

        # Sửa lỗi URL thiếu chính xác
        if not src.startswith("http"):
            src = "https://sinhvien.huit.edu.vn" + src

        # Tải ảnh
        response = requests.get(src)
        if response.status_code == 200:
            file_path = os.path.join(SAVE_DIR, f"{i}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Đã lưu ảnh {file_path}")
        else:
            print(f"❌ Không thể tải ảnh: {src}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    time.sleep(1)  # đợi CAPTCHA mới sinh ra

driver.quit()
print("\n🎉 Đã hoàn tất thu thập ảnh.")
