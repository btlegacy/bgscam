import requests
import os
from datetime import datetime

URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"
IMAGE_DIR = "images"

def main():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{IMAGE_DIR}/{timestamp}.jpg"
    
    try:
        response = requests.get(URL, timeout=20)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Captured: {filename}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
