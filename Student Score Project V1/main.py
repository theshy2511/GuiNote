# main.py
import argparse
from capsolver_client import CapSolverClient
from scraper import Scraper
from utils import read_input_excel, write_output_excel, get_capsolver_key
import pandas as pd
import time

DEFAULT_BASE_URL = 'https://sinhvien.huit.edu.vn/tra-cuu-thong-tin.html'

# default selectors - **MUST** be adapted to the target site
DEFAULT_SELECTORS = {
    'mssv_input': "//input[contains(@placeholder,'Mã sinh viên') or contains(@placeholder,'Nhập mã sinh viên') or contains(@name,'mssv')]",
    'captcha_img': "//img[contains(@id,'captcha') or contains(@src,'captcha') or contains(@class,'captcha')]",
    'captcha_input': "//input[@name='captcha' or contains(@placeholder,'Nhập mã')]",
    'submit_button': "//button[contains(.,'Tra cứu') or contains(.,'Tra cuu') or contains(.,'Tra cứu')]",
    'view_score_button': "//a[contains(.,'Xem điểm') or contains(.,'XEM ĐIỂM')]",
}

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--sheet', default='HocBong')
    p.add_argument('--output', default='results.xlsx')
    p.add_argument('--mssv-col', default='mssv')
    p.add_argument('--semester')
    p.add_argument('--course')
    p.add_argument('--teacher')
    p.add_argument('--headless', action='store_true')
    p.add_argument('--base-url', default=DEFAULT_BASE_URL)
    return p.parse_args()

def main():
    args = parse_args()
    df = read_input_excel(args.input, args.sheet, args.mssv_col)
    cap_key = get_capsolver_key()
    if not cap_key:
        raise RuntimeError('CAPSOLVER_API_KEY not set in environment (.env)')

    client = CapSolverClient(cap_key)
    scraper = Scraper(headless=args.headless)

    out = df.copy()
    out['Processed'] = False
    out['Error'] = ''
    out['GPA'] = None
    out['TotalTC'] = None
    out['Details'] = ''

    try:
        for idx, row in df.iterrows():
            mssv = str(row[args.mssv_col]).strip()
            if not mssv or pd.isna(mssv):
                out.at[idx, 'Error'] = 'Empty mssv'
                # save progress and continue
                write_output_excel(out, args.output)
                continue

            try:
                res = scraper.fetch_score_for_mssv(args.base_url, mssv, client, DEFAULT_SELECTORS)
                rows = res.get('rows', [])
                # parse rows (example heuristic, adapt to actual table layout)
                total_tc = 0
                total_weighted = 0.0
                details = []
                for r in rows:
                    # assume r like [no, code, name, tc, score]
                    if len(r) >= 5:
                        try:
                            tc = int(r[3])
                        except:
                            tc = 0
                        try:
                            score = float(r[4].replace(',', '.'))
                        except:
                            score = 0.0
                        total_tc += tc
                        total_weighted += tc * score
                        details.append('|'.join([str(x) for x in r]))
                gpa = round(total_weighted / total_tc, 2) if total_tc else None

                out.at[idx, 'Processed'] = True
                out.at[idx, 'GPA'] = gpa
                out.at[idx, 'TotalTC'] = total_tc
                out.at[idx, 'Details'] = ';'.join(details)

            except Exception as e:
                # per-row error handling
                out.at[idx, 'Error'] = str(e)

            # save progress every iteration
            write_output_excel(out, args.output)
            # polite delay to avoid hammering the site
            time.sleep(0.6)

    finally:
        # always close scraper and write final output
        try:
            scraper.close()
        except Exception:
            pass
        write_output_excel(out, args.output)

if __name__ == '__main__':
    main()
