import requests
from bs4 import BeautifulSoup
import argparse
import os
from PIL import Image
from io import BytesIO
import time
from get_images_funcs import get_image_urls_via_scraping, get_image_urls_via_api

# Set up script
parser = argparse.ArgumentParser(description="Save county images from Wikipedia")
parser.add_argument(
    "--save-folder",
    type=str,
    default="data",
    help="Path to the folder where images will be saved, relative to directory where script is located (default: data)"
)
parser.add_argument(
    "--use-api",
    type=bool,
    default=False,
    help="Use the Wikipedia API to get image URLs (default: False i.e. use scraping)"
)

# Create a data folder if none exists for images
args = parser.parse_args()
save_folder = args.save_folder
os.makedirs(save_folder, exist_ok=True)

# List of counties in England
counties = [
    "Bedfordshire",
    "Berkshire",
    "Bristol",
    "Buckinghamshire",
    "Cambridgeshire",
    "Cheshire",
    "City of London",
    "Cornwall",
    "Cumbria",
    "Derbyshire",
    "Devon",
    "Dorset",
    "County Durham",
    "East Riding of Yorkshire",
    "East Sussex",
    "Essex",
    "Gloucestershire",
    "Greater London",
    "Greater Manchester",
    "Hampshire",
    "Herefordshire",
    "Hertfordshire",
    "Isle of Wight",
    "Kent",
    "Lancashire",
    "Leicestershire",
    "Lincolnshire",
    "Merseyside",
    "Norfolk",
    "North Yorkshire",
    "Northamptonshire",
    "Northumberland",
    "Nottinghamshire",
    "Oxfordshire",
    "Rutland",
    "Shropshire",
    "Somerset",
    "South Yorkshire",
    "Staffordshire",
    "Suffolk",
    "Surrey",
    "Tyne and Wear",
    "Warwickshire",
    "West Midlands",
    "West Sussex",
    "West Yorkshire",
    "Wiltshire",
    "Worcestershire"
]

# URL = "https://en.wikipedia.org/wiki/Counties_of_England#Ceremonial_counties"
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

#Get URL for the wikipedia article for each county
updated_counties = [county.replace(" ", "_") if " " in county else county for county in counties]
urls = [f"https://en.wikipedia.org/wiki/{county}" for county in updated_counties]
# Slightly ugly cheat for the West Midlands
for i, url in enumerate(urls):
    if updated_counties[i] != "West_Midlands":
        continue
    else:
        urls[i] += "_(county)"

# print(img_urls)

if not args.use_api:
    img_urls = get_image_urls_via_scraping(urls, updated_counties)

    # Scrape images and save them
    for county, image_url in img_urls.items():
        if not image_url:
            print(f"No image URL found for {county}")
            continue
        output_path = os.path.join(save_folder, f"{county}.jpg")
        if os.path.isfile(output_path):
            print(f"Image for {county} already exists at {output_path}. Skipping. Please delete this image if you would like an updated one.")
            continue

        # Tried repeating requests when got a 403 but this wasn't successful
        # attempts = 0
        # while attempts <= 10:
        #     attempts += 1
        #     response = requests.get(image_url)
        #     if response.status_code == 403:
        #         print(f"403 error for {county}. Trying again. Attempt {attempts}")
        #         time.sleep(2)
        #     else:
        #         break

        headers = {"User-Agent": "AnkiImagesBot/0.0 (https://github.com/isobelweinberg)"}
        session = requests.Session()
        session.headers.update(headers)

        response = session.get(url)

        response = requests.get(image_url, headers=headers)
        if response.status_code == 200:
            try:
                # Convert to JPEG
                image = Image.open(BytesIO(response.content))
                if image.mode == 'RGBA':
                    background = Image.new('RGB', image.size, (255, 255, 255))  # White background
                    background.paste(image, mask=image.split()[3])  # Paste the PNG image onto the white background
                    image = background
                image.convert("RGB").save(output_path, "JPEG")
                print(f"Image for {county} has been saved successfully at {output_path}")
            except Exception as e:
                print(f"Failed to process image for {county}: {e}")
        else:
            print(f"Failed to retrieve image for {county}. Status code: {response.status_code}")
        time.sleep(2)

elif args.use_api:
    # Decided to leave this code here. Testing out a new way to get the images via the API rather than scraping. 
    # The reason for doing this was because was getting quite a few 403 errors when trying to scrape the images
    # However, still needs quite a lot more work to get only the right images, so decided to continue with the web scraping and add management of the 403s

    for i, county in enumerate(updated_counties):
        print(county)
        image_filenames, image_urls = get_image_urls_via_api(county)
        for j in image_filenames:
            # print(counties[i] + ' UK')
            if counties[i] + ' UK' in j:
                print(j)
            
        