import requests
from datetime import datetime
import os

# URL of the webcam
url = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"

def download_image():
    # Create folder if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"images/webcam_{timestamp}.jpg"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Successfully saved: {filename}")
        else:
            print(f"Failed to download. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_image()
