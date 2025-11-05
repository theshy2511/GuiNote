import os
import base64
import time
import requests

API_URL = os.environ.get("CAPSOLVER_API_URL", "https://api.your-capsolver.com/solve")  # sửa theo docs
API_KEY = os.environ.get("CAPSOLVER_API_KEY")  # set trong env, không hardcode

class CaptchaSolveError(Exception):
    pass

def solve_captcha_from_bytes(image_bytes: bytes, timeout: int = 30, max_retries: int = 3) -> str:
    """
    Gửi ảnh captcha (bytes) tới CapSolver, trả về kết quả text.
    Thay payload/headers/field theo docs của nhà cung cấp.
    """
    if not API_KEY:
        raise CaptchaSolveError("CAPSOLVER_API_KEY chưa được đặt trong env")

    b64 = base64.b64encode(image_bytes).decode('ascii')
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        # thêm header khác nếu nhà cung cấp yêu cầu
    }

    payload = {
        # ví dụ chung: "type": "image_base64", "image": b64
        # chỉnh theo docs: nhiều dịch vụ dùng multipart/form-data thay vì json
        "type": "image_base64",
        "image": b64,
        # "task": "capsolver_text", ...
    }

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=timeout)
        except requests.RequestException as e:
            if attempt >= max_retries:
                raise CaptchaSolveError(f"Yêu cầu tới CapSolver thất bại: {e}")
            time.sleep(1 + attempt)
            continue

        if resp.status_code != 200:
            # lỗi dịch vụ hoặc key sai
            msg = f"CapSolver trả mã lỗi {resp.status_code}: {resp.text}"
            if attempt >= max_retries:
                raise CaptchaSolveError(msg)
            time.sleep(1 + attempt)
            continue

        # parse response JSON — thay key theo docs
        try:
            data = resp.json()
        except ValueError:
            raise CaptchaSolveError("Không parse được JSON từ CapSolver")

        # --- CHỖ NÀY CẦN CHỈNH theo response thực tế ---
        # ví dụ: {"success": True, "result": "ABC123"}
        if data.get("success") and data.get("result"):
            return data["result"]
        # nhiều API trả task_id rồi phải poll -> ví dụ code polling:
        if data.get("task_id"):
            task_id = data["task_id"]
            # poll result
            for _ in range(15):
                poll = requests.get(f"{API_URL}/result/{task_id}", headers=headers, timeout=timeout)
                if poll.status_code == 200:
                    p = poll.json()
                    if p.get("status") == "done" and p.get("text"):
                        return p["text"]
                time.sleep(1)
            raise CaptchaSolveError("Timeout khi poll kết quả ở CapSolver")
        # nếu đến đây, coi như không có kết quả
        if attempt >= max_retries:
            raise CaptchaSolveError(f"CapSolver không trả kết quả hợp lệ: {data}")
        time.sleep(1 + attempt)
