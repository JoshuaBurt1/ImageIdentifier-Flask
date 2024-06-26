from playwright.sync_api import sync_playwright
import time
import requests
import os
from bs4 import BeautifulSoup

# ALERT: Run py _webscrape_mushroomVal.py first to get the folder_names array
# Function to scrape images from iNaturalist.ca; (06-25-2024) -> adds to train folder data; mushroom_dataset/train/...
# NOTE: Downloaded data includes microscope & distance images that must be filtered through for best base unit distance identification results 
def scrape_iNaturalistM(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        #WEBPAGE 1
        page.goto(url)
        # Wait for the page to load and stabilize
        page.wait_for_load_state("networkidle")
        # Path to the directory containing your dataset
        dataset_path = 'mushroom_dataset/val'
        folder_names = [folder for folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, folder))]
        #print(folder_names)
        #print(len(folder_names))
        #print(folder_names[j])

        # Query page to see if there is a resource page for one of the elements of folder_names    
        for j in range(0,len(folder_names)):
            page.fill('input[name="taxon_name"]', folder_names[j])
            page.wait_for_load_state("networkidle")
            time.sleep(1)    
            #content = page.content()
            href_values = page.evaluate('''() => {
                const elements = document.querySelectorAll('.ac-view');
                const hrefs = [];
                elements.forEach(element => {
                    hrefs.push(element.href);
                });
                return hrefs;
            }''')            
            if href_values:
                print("Href values of elements with class 'ac-view':")
                print(href_values[0])
            else:
                mkSave_folder(folder_names[j])
                print(f"No href values found for {folder_names[j]}.")
                continue 

            #WEBPAGE 2
            page.goto(href_values[0])
            page.wait_for_load_state("networkidle")
            #content = page.content()
            print(f"\nSpecies: {folder_names[j]}")
            #print(content)
            current_url = page.url
            #print(f"\nCurrent URL: {current_url}")

            #WEBPAGE 3 : # Gets to this type of page: https://inaturalist.ca/taxa/499795-Agaricus-auricolor/browse_photos
            current_url = current_url + '/browse_photos?layout=grid'
            page.goto(current_url)
            print(f"\nCurrent URL: {current_url}")
            page.wait_for_load_state("networkidle")
            for scroll in range(0,2): #gets ~50-100 results per species; increase range to get more image urls (if they exist)
                wait(page)
                print(f"Scroll: {scroll}")
            content_after_scroll = page.content()
            print("Content after scrolling for 1 second:")
            #with open('iNaturalistContent3.txt', 'a', encoding='utf-8') as file:
            #    file.write(content_after_scroll3)
            
            # Find the start and end indices of the object
            start_index = content_after_scroll.find('<div id="app"><div id="Photos">')
            end_index = content_after_scroll.find('<div class="bootstrap" id="footer">', start_index)

            # Extract the portion containing the image urls (Find all instances of "https://inaturalist")
            if start_index != -1 and end_index != -1:
                js_object_str = content_after_scroll[start_index:end_index].strip()
                print(js_object_str)
                urls = []
                index = 0
                while index != -1:
                    index = js_object_str.find("https://inaturalist", index)
                    if index != -1:
                        end_index = js_object_str.find('"', index)
                        if end_index != -1:
                            url = js_object_str[index:end_index]
                            urls.append(url)
                            index = end_index
                        else:
                            break
                
                # Make a list of unique and working urls to avoid downloading same pictures
                print("Array of URLs:")
                #print(urls) ###
                print(f"Initial url amount: {len(urls)}")
                unique_parameters = set()
                unique_urls = []
                for url in urls:
                    url_parts = url.split('/')
                    for parameter in url_parts:                      # Extract the pure number parameter
                        if parameter.isdigit() and parameter not in unique_parameters:
                            unique_parameters.add(parameter)
                            unique_urls.append(url)
                # Change the image size to original file size for best resolution
                for i in range(len(unique_urls)):
                    unique_urls[i] = unique_urls[i].replace('&quot;);', '')
                    unique_urls[i] = unique_urls[i].replace('thumb', 'original')
                    unique_urls[i] = unique_urls[i].replace('square', 'original')
                    unique_urls[i] = unique_urls[i].replace('small', 'original')
                    unique_urls[i] = unique_urls[i].replace('medium', 'original')
                    unique_urls[i] = unique_urls[i].replace('large', 'original')
                # Filter out URLs that don't end with .jpg, .jpeg, or .png
                filtered_urls = []
                for urlF in unique_urls:
                    parts = urlF.split('.')
                    if parts[-1] in ['jpg', 'jpeg', 'png']:
                        filtered_urls.append(urlF)
                print(filtered_urls)
                print(f"Filtered urls: {len(filtered_urls)}")

                # Check for obtaining highest resolution image
                for i2 in range(len(filtered_urls)):
                    if 'original' not in filtered_urls[i2]:
                        print("Unknown image type found.")
                        break
                print(f"Filtered url amount: {len(filtered_urls)}")
                print(folder_names[j])

                # Download the images
                if len(filtered_urls)>0:
                    for url in filtered_urls:
                        download_image(url, folder_names[j])
                else: #still make a save folder
                    mkSave_folder(folder_names[j])
        browser.close()

def mkSave_folder(folder_name):
    save_folder = f"mushroom_dataset/train/{folder_name}"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

# Function to download images
def download_image(url, folder_name):
    response = requests.get(url)
    if response.status_code == 200:
        #filename = folder_name+url.split('.')[-1]
        save_folder = f"mushroom_dataset/train/{folder_name}"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        count = len([name for name in os.listdir(save_folder) if os.path.isfile(os.path.join(save_folder, name))])
        filename = folder_name+"_"+str(count)+"."+url.split('.')[-1]
        filename = filename.replace(' ', '_')
        file_path = os.path.join(save_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded: {filename} to {save_folder}/{filename}")

def wait(page):
    page.evaluate('''() => {
                window.scrollTo(0, document.body.scrollHeight);
            }''')
    time.sleep(1)    
    page.wait_for_load_state("networkidle")

if __name__ == "__main__":
    url = "https://inaturalist.ca/observations?place_id=any&subview=map"
    scrape_iNaturalistM(url)
    