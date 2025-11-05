# capsolver_client.py

import time
import base64
import requests

class CapSolverError(Exception):
    pass

class CapSolverClient:
    CREATE_URL = "https://api.capsolver.com/createTask"
    GET_URL = "https://api.capsolver.com/getTaskResult"

    def __init__(self, api_key, poll_interval=1.5, timeout=60):
        self.api_key = api_key
        self.poll_interval = poll_interval
        self.timeout = timeout


    def solve_image(self, image_bytes):
        """Send ImageToTextTask to CapSolver and return solved text."""
        b64 = base64.b64encode(image_bytes).decode('utf-8')
        payload = {
            "clientKey": self.api_key,
            "task": {
            "type": "ImageToTextTask",
            "body": b64
            }
        }
        r = requests.post(self.CREATE_URL, json=payload, timeout=20)
        r.raise_for_status()
        j = r.json()
        if j.get("errorId"):
            raise CapSolverError(f"createTask error: {j}")
        task_id = j.get("taskId")
        if not task_id:
            raise CapSolverError(f"no taskId in response: {j}")

        start = time.time()
        while True:
            if time.time() - start > self.timeout:
                raise CapSolverError("Timeout waiting for capsolver result")
            time.sleep(self.poll_interval)
            r2 = requests.post(self.GET_URL, json={"clientKey": self.api_key, "taskId": task_id}, timeout=20)
            r2.raise_for_status()
            j2 = r2.json()
            if j2.get("status") == "ready":
                sol = j2.get("solution")
                if isinstance(sol, dict) and "text" in sol:
                    return sol["text"]
                return str(sol)
            if j2.get("errorId"):
                raise CapSolverError(f"getTaskResult error: {j2}")


    def solve_recaptcha(self, website_url, site_key):
        """Example for ReCaptcha V2 proxyless - modify if needed."""
        payload = {
            "clientKey": self.api_key,
            "task": {
            "type": "RecaptchaV2TaskProxyless",
            "websiteURL": website_url,
            "websiteKey": site_key
            }
        }
        r = requests.post(self.CREATE_URL, json=payload, timeout=20)
        r.raise_for_status()
        j = r.json()
        if j.get("errorId"):
            raise CapSolverError(f"createTask error: {j}")
        task_id = j.get("taskId")
        start = time.time()
        while True:
            if time.time() - start > self.timeout:
                raise CapSolverError("Timeout waiting for capsolver result")
            time.sleep(self.poll_interval)
            r2 = requests.post(self.GET_URL, json={"clientKey": self.api_key, "taskId": task_id}, timeout=20)
            r2.raise_for_status()
            j2 = r2.json()
            if j2.get("status") == "ready":
                sol = j2.get("solution")
                return sol
            if j2.get("errorId"):
                raise CapSolverError(f"getTaskResult error: {j2}")