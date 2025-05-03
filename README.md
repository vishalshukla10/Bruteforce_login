# Bruteforce_login

An advanced Python-based web login bruteforcer for penetration testing and ethical hacking. Supports CSRF token extraction, multi-threading, proxy/Tor routing, lockout detection, logging, and HTML reporting.

## 🧰 Features

    CSRF Token support
    Multi-threaded login attempts
    Proxy & Tor routing support
    CAPTCHA / lockout detection
    Output logging to `bruteforce_log.txt`
    Auto HTML report generation on success

---

## 🛠️ Requirements

    * Python 3.7+
    * Kali Linux (recommended)
    * Install dependencies:

```bash
pip install requests beautifulsoup4
```

If using Tor routing:

```bash
sudo apt install tor
pip install requests[socks]
sudo service tor start
```

---

## ⚙️ Configuration

Edit these variables in `bruteforce_login.py`:

```python
TARGET_URL = "http://192.168.1.100/dvwa/login.php"
USERNAME = "admin"
WORDLIST = "/usr/share/wordlists/rockyou.txt"
CSRF_FIELD = "user_token"  # Update based on form input name
USE_TOR = False  # Set to True to use Tor
```

---

## 🚀 Usage

```bash
python3 bruteforce_login.py
```

* Logs are saved to: `bruteforce_log.txt`
* Successful login report: `bruteforce_report.html`

---

## 📁 Example Output

```
[2025-05-03 12:21:15] Starting brute-force on http://192.168.1.100/dvwa/login.php as 'admin'...
[2025-05-03 12:21:29] Password found: password123
[+] HTML report saved to bruteforce_report.html
```

---

## 🔒 Disclaimer

This tool is intended for educational use and legal penetration testing only. Do **not** use on systems you do not own or have explicit permission to test.

---

## 📄 License

MIT License

---

## 💡 Author

Created with ❤️ for ethical hacking labs and CTF practice.

---
