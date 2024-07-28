import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Set up a session with retry logic
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def download_image(url, path):
    if os.path.exists(path):
        print(f"File already exists, skipping: {path}")
        return

    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {path}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {str(e)}")

def process_gallery(base_url, url, base_path, visited=None):
    if visited is None:
        visited = set()

    full_url = urllib.parse.urljoin(base_url, url)
    if full_url in visited:
        return

    visited.add(full_url)
    print(f"Processing gallery: {full_url}")

    subfolders = []
    images = []
    current_path = base_path

    while full_url:
        try:
            response = session.get(full_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing URL {full_url}: {str(e)}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Collect subfolders, excluding navigation links
        new_subfolders = soup.find_all('a', href=lambda href: href and 'f=' in href)
        new_subfolders = [sf for sf in new_subfolders if sf.text.strip().lower() not in ['up', 'next', 'previous']]
        subfolders.extend(new_subfolders)

        # Collect images
        new_images = soup.find_all('a', href=lambda href: href and 'i=' in href)
        images.extend(new_images)

        # Check for "Next" link
        next_link = soup.find('a', string='Next')
        if next_link:
            full_url = urllib.parse.urljoin(base_url, next_link['href'])
            print(f"Moving to next page: {full_url}")
        else:
            full_url = None  # No more pages, exit the loop

    # Process all collected images
    print(f"Found {len(images)} potential images")
    for img in images:
        img_page_url = urllib.parse.urljoin(base_url, img['href'])
        print(f"Processing image page: {img_page_url}")
        try:
            img_page = session.get(img_page_url, timeout=30)
            img_page.raise_for_status()
            img_soup = BeautifulSoup(img_page.text, 'html.parser')
            full_img_link = img_soup.find('a', href=lambda href: href and href.endswith(('.jpg', '.png', '.gif')))
            if full_img_link:
                full_img_url = urllib.parse.urljoin(base_url, full_img_link['href'])
                print(f"Full size image URL: {full_img_url}")
                file_name = os.path.basename(full_img_url)
                download_image(full_img_url, os.path.join(current_path, file_name))
            else:
                print(f"No full-size image found on page: {img_page_url}")
        except requests.RequestException as e:
            print(f"Error processing image page {img_page_url}: {str(e)}")
        time.sleep(1)  # Be polite to the server

    # Process subfolders
    print(f"Found {len(subfolders)} potential subfolders")
    for subfolder in subfolders:
        subfolder_url = urllib.parse.urljoin(base_url, subfolder['href'])
        subfolder_name = subfolder.find('img')['alt'] if subfolder.find('img') else subfolder.text.strip()
        if subfolder_name and subfolder_name.lower() not in ['up', 'next', 'previous']:
            print(f"Processing subfolder: {subfolder_name} ({subfolder_url})")
            subfolder_path = os.path.join(base_path, subfolder_name)
            process_gallery(base_url, subfolder_url, subfolder_path, visited)

# Main execution
base_url = "https://brickshelf.com"
start_url = "/cgi-bin/gallery.cgi?m=username"
local_base_path = os.path.expanduser("~/Desktop/brickshelf_download")

print(f"Starting download process. Files will be saved to: {local_base_path}")

try:
    os.makedirs(local_base_path, exist_ok=True)
    print(f"Created directory: {local_base_path}")
except Exception as e:
    print(f"Error creating directory: {str(e)}")

process_gallery(base_url, start_url, local_base_path)
print("Download process completed.")

print(f"Contents of the download directory: {os.listdir(local_base_path) if os.path.exists(local_base_path) else 'N/A'}")