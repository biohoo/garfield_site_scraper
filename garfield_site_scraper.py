import os
import time
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import datetime 

START_YEAR = 2024
END_YEAR = datetime.datetime.now().year

# Base URL of the webpage
base_url = 'http://pt.jikos.cz/garfield/'

# Output directory for images
output_directory = 'downloaded_images'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Configure retry strategy
retry_strategy = Retry(
    total=3,  # number of retries
    backoff_factor=1,  # wait 1, 2, 4 seconds between retries
    status_forcelist=[429, 500, 502, 503, 504]  # HTTP status codes to retry on
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

def get_images(url_in):
    try:
        # Request the webpage with retry mechanism
        print(f"Requesting {url_in}")
        response = session.get(url_in, timeout=10)
        if response.status_code != 200:
            print(f"Failed to access {url_in} - Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract image URLs
        image_tags = soup.find_all('img')
        image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

        # Download images
        for url in image_urls:
            # Skip download if image already exists
            if os.path.basename(url) in os.listdir('downloaded_images'):
                print(f'Image found in directory. Skipping: {os.path.basename(url)}')
                continue
            
            # Skip footer images
            if 'valid' in os.path.basename(url) or 'vim.gif' in os.path.basename(url):
                continue
            
            try:
                # Add delay between downloads to be nice to the server
                time.sleep(1)
                
                # Construct the absolute URL for the image if needed
                if not url.startswith(('http://', 'https://')):
                    url = base_url + url if url.startswith('/') else base_url + '/' + url
                
                response = session.get(url, timeout=10)
                if response.status_code == 200:
                    filename = os.path.join(output_directory, os.path.basename(url))
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded image: {os.path.basename(url)}")
                else:
                    print(f"Failed to download image: {url} - Status code: {response.status_code}")
            except Exception as e:
                print(f"Error downloading image {url}: {str(e)}")
                time.sleep(5)  # Wait longer on error
                continue

    except Exception as e:
        print(f"Error accessing page {url_in}: {str(e)}")
        time.sleep(5)  # Wait longer on error
        return

if __name__ == "__main__":
    for year in range(START_YEAR, END_YEAR + 1):
        if year == datetime.datetime.now().year:
            end_month = datetime.datetime.now().month + 1
        else:
            end_month = 13
        for month in range(1, end_month):
            url = f"{base_url}{year}/{month}"
            get_images(url)
