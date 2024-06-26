from playwright.sync_api import sync_playwright
import requests
import os
import shutil
from bs4 import BeautifulSoup

# Function to scrape images from MushroomExpert.com (06-24-2024) -> adds to val folder data; mushroom_dataset/val/...
# NOTE: There are microscope images in thumbs that have not been downloaded (microscope thumbs = unassociated thumbs - downloaded&thumbs)
def scrape_mushroomexpert(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # Wait for the page to load and stabilize
        page.wait_for_load_state("networkidle")
        
        content = page.content()

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        body = soup.find('body')
        
        if body:
            center = body.find('center')
            if center:
                a_tag = center.find('a')
                if a_tag:
                    # Adjust the logic to find the correct table based on your specific requirements
                    tables = center.find_all('table')
                    if len(tables) >= 3:
                        last_table = tables[2]
                        links = last_table.find_all('a', href=True) #first a tag to avoid duplicates
                        link_urls_set = set() # removes duplicates
                        for link in links:
                            link_url = url + link['href']
                            link_urls_set.add(link_url)
                        link_urls = sorted(link_urls_set)
                        #print(link_urls)

                        print("\nAll link URLs from the third table (sorted alphabetically):")
                        for full_url in link_urls:
                            # Navigate to the link URL using Playwright
                            page.goto(full_url)
                            page.wait_for_load_state("networkidle")
                            link_content = page.content()
                            
                            # Parse the content of the link's page to find images
                            link_soup = BeautifulSoup(link_content, 'html.parser')
                            image_links = link_soup.find_all('a', href=True)
                            #print(image_links)
                            
                            # Filter and download only images that start with "images/"
                            for image_link in image_links:
                                image_url = image_link['href']
                                if image_url.startswith('images/'):
                                    full_image_url = url + image_url
                                    download_image(full_image_url)
                                    print(full_image_url)
        browser.close()

# Function to download images
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        binomial_nomenclature = convert_to_binomial(filename)
        save_folder = f"mushroom_dataset/val/{binomial_nomenclature}"
        
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        file_path = os.path.join(save_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
            #print(f"Downloaded: {filename} to {save_folder}/{filename}")

# Function to convert filename to binomial nomenclature
def convert_to_binomial(filename):
    parts = filename.split('_')
    species_name_parts = []
    for part in parts:
        if any(char.isdigit() for char in part):
            continue
        species_name_parts.append(part)
    species_name = ' '.join(species_name_parts).capitalize()
    return species_name

#some folders that contain information end in .jpg, thumb.jpg, non-standard binomial form; rename and merge if required
def rename_folders():
    base_dir = "mushroom_dataset/val"
    for folder_name in os.listdir(base_dir):
        old_path = os.path.join(base_dir, folder_name)
        new_folder_name = folder_name.replace(" thumb.jpg", "").replace(".jpg", "")
        if new_folder_name == folder_name:
            continue 
        new_path = os.path.join(base_dir, new_folder_name)
        if os.path.exists(new_path):
            merge_folders(old_path, new_path)
        else:
            os.rename(old_path, new_path)
            print(f"Renamed folder '{folder_name}' to '{new_folder_name}'")
    dataset_path = 'mushroom_dataset/val'
    folder_names = [folder for folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, folder))]
    print(folder_names)
    #amend non-standard naming convention
    for name in folder_names:
        parts = name.split(' ')
        count_parts = len(parts)
        if count_parts > 2:
            new_name = parts[-2].capitalize() + ' ' + parts[-1]
            old_path = os.path.join(dataset_path, name)
            new_path = os.path.join(dataset_path, new_name)
            if os.path.exists(new_path):
                merge_folders(old_path, new_path)
                print("Merged")
            else:
                os.rename(old_path, new_path)
                print(f"Modified folder '{name}' to '{new_name}'")
                #other modification: Xerampelina group -> Russula xerampelina

# Function to merge contents of source folder into destination folder
def merge_folders(source, destination):
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)
        if os.path.isdir(source_item):
            merge_folders(source_item, destination_item)
        else:
            shutil.move(source_item, destination_item)
    os.rmdir(source)

if __name__ == "__main__":
    url = "https://www.mushroomexpert.com/"
    #scrape_mushroomexpert(url)
    rename_folders()