#Function to scrape images from iNaturalist (VAL OR TRAIN DATA) #should be TRAIN as larger

# Get to this type of page
# https://inaturalist.ca/taxa/499795-Agaricus-auricolor/browse_photos
# https://inaturalist.ca/taxa/352689-Tylopilus-ferrugineus/browse_photos

from playwright.sync_api import sync_playwright
import requests
import os
from bs4 import BeautifulSoup

def scrape_iNaturalistM(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # Wait for the page to load and stabilize
        page.wait_for_load_state("networkidle")
        content = page.content()
        print(content)

if __name__ == "__main__":
    url = "https://inaturalist.ca/observations"
    scrape_iNaturalistM(url)
    # Path to the directory containing your dataset
    dataset_path = 'mushroom_dataset/val'
    folder_names = [folder for folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, folder))]
    print(folder_names)