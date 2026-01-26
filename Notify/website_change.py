import requests
import hashlib
import smtplib
import time
from email.mime.text import MIMEText

# --- Configuration ---
URL_TO_MONITOR = "https://example.com"
CHECK_INTERVAL = 3600  # Seconds (e.g., 3600 = 1 hour)
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use an App Password, not your main password
EMAIL_RECEIVER = "destination@example.com"

def get_site_hash():
    """Fetches the website content and returns its SHA-256 hash."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL_TO_MONITOR, headers=headers)
    return hashlib.sha256(response.text.encode('utf-8')).hexdigest()

def send_notification():
    """Sends a simple email alert."""
    msg = MIMEText(f"Change detected on {URL_TO_MONITOR}!")
    msg['Subject'] = 'Website Change Alert'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    print("Email sent!")

def monitor():
    print(f"Monitoring {URL_TO_MONITOR}...")
    try:
        # Get the initial state
        current_hash = get_site_hash()
        
        while True:
            time.sleep(CHECK_INTERVAL)
            new_hash = get_site_hash()
            
            if new_hash != current_hash:
                print("Change detected!")
                send_notification()
                current_hash = new_hash
            else:
                print("No change.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    monitor()
