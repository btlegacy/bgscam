import requests
from datetime import datetime
import os

URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"

def capture():
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Timestamp for the filename
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename = f"images/{timestamp}.jpg"
    
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Saved {filename}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capture()
