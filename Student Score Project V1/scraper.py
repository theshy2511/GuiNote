# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import base64

class Scraper:
    def __init__(self, headless=False, timeout=20):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, timeout)

    def close(self):
        try:
            self.driver.quit()
        except:
            pass

    def fetch_score_for_mssv(self, base_url, mssv, capsolver_client, selectors):
        """Return a dict with result fields or raise exception."""

        driver = self.driver
        driver.get(base_url)

        # fill mssv
        mssv_input = self.wait.until(EC.presence_of_element_located((By.XPATH, selectors['mssv_input'])))
        mssv_input.clear()
        mssv_input.send_keys(mssv)

        # captcha img
        cap_img_el = self.wait.until(EC.presence_of_element_located((By.XPATH, selectors['captcha_img'])))
        src = cap_img_el.get_attribute('src')
        if src and src.startswith('data:'):
            header, b64 = src.split(',', 1)
            img_bytes = base64.b64decode(b64)
        elif src:
            import requests
            r = requests.get(src, timeout=15)
            r.raise_for_status()
            img_bytes = r.content
        else:
            img_bytes = cap_img_el.screenshot_as_png

        cap_text = capsolver_client.solve_image(img_bytes)
        cap_input = driver.find_element(By.XPATH, selectors['captcha_input'])
        cap_input.clear()
        cap_input.send_keys(cap_text)

        # click submit
        submit_btn = driver.find_element(By.XPATH, selectors['submit_button'])
        submit_btn.click()
        time.sleep(1)

        # optionally click view score
        if 'view_score_button' in selectors:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selectors['view_score_button'])))
                btn.click()
                time.sleep(0.8)
            except:
                pass

        # parse page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # the parsing below is generic: user should adapt to actual page
        table = soup.find('table')
        if not table:
            raise RuntimeError('No score table found')

        # collect rows
        rows = []
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cells:
                rows.append(cells)

        # return raw rows for main to process
        return {'mssv': mssv, 'rows': rows}
