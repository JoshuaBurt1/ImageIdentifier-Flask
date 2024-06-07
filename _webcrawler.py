import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def download_image(url, folder_path):
    try:
        if url.startswith('//'):
            url = 'https:' + url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(folder_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        print("Error occurred while downloading image:", e)

def crawl_website_for_images(website_url, animal_name, save_folder):
    try:
        response = requests.get(website_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            for img in images:
                img_url = img.get('src')
                if img_url and animal_name in img_url:
                    print("Found image:", img_url)
                    # Follow the link to the image page to get the direct URL
                    image_page_url = img.parent.get('href')
                    if not image_page_url.startswith('http'):
                        image_page_url = urljoin(website_url, image_page_url)
                    image_url = get_high_resolution_image_url(image_page_url)
                    if image_url:
                        print("Direct image URL:", image_url)
                        image_name = image_url.split('/')[-1]
                        image_path = os.path.join(save_folder, animal_name, image_name)
                        download_image(image_url, image_path)
    except Exception as e:
        print("Error occurred while crawling website:", e)

def get_high_resolution_image_url(image_page_url):
    try:
        response = requests.get(image_page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for the high resolution image URL in the page
            high_res_img = soup.find('div', class_='fullImageLink').find('a').get('href')
            return high_res_img
    except Exception as e:
        print("Error occurred while getting high resolution image URL:", e)
    return None

def main():
    animals = {
        "White-tailed_deer": [
            "https://en.wikipedia.org/wiki/Deer",
            "https://en.wikipedia.org/wiki/White-tailed_deer",
        ],
        "elephant": [
            "https://en.wikipedia.org/wiki/Elephant",
            "https://en.wikipedia.org/wiki/African_elephant",
        ],
        "Elephant": [
            "https://en.wikipedia.org/wiki/Elephant",
            "https://en.wikipedia.org/wiki/African_elephant",
        ],
        # Add more animals and their URLs as needed
    }

    save_folder = "webcrawler_images"

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for animal, websites in animals.items():
        animal_folder = os.path.join(save_folder, animal)
        if not os.path.exists(animal_folder):
            os.makedirs(animal_folder)
        for website in websites:
            crawl_website_for_images(website, animal, save_folder)

if __name__ == "__main__":
    main()