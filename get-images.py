import requests
from bs4 import BeautifulSoup
import argparse
import os

# Set up script
parser = argparse.ArgumentParser(description="Save county images from Wikipedia")
parser.add_argument(
    "--save-folder",
    type=str,
    default="data",
    help="Path to the folder where images will be saved, relative to directory where script is located (default: data)"
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
        urls[i] += "_(region)"

# Get image URLs from wikipedia
img_urls = {}

for i, url in enumerate(urls):   
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", class_="infobox ib-settlement vcard")
    img_urls[updated_counties[i]] = None
    if table:
        specific_cells = table.find_all("td", class_="infobox-full-data")
        if len(specific_cells) > 1:
            cell_with_img = specific_cells[1]
            img_tag = cell_with_img.find("img")
            if not img_tag:
                cell_with_img = specific_cells[2] if len(specific_cells) > 2 else None
                img_tag = cell_with_img.find("img") if cell_with_img else None
            if img_tag and "src" in img_tag.attrs:
                img_urls[updated_counties[i]] = 'https:' + img_tag["src"].replace("250", "500")
            else: 
                print(f"No image found in relevant cell at {url}")
        else:
            print(f"Only {len(specific_cells)} cells found at {url}")
    else:
        print(f"No table found at {url}")

# print(img_urls)

# Scrape images and save them
for county, image_url in img_urls.items():
    if not image_url:
        print(f"No image URL found for {county}")
        continue
    output_path = os.path.join(save_folder, f"{county}.png")
    if os.path.isfile(output_path):
        print(f"Image for {county} already exists at {output_path}. Skipping. Please delete this image if you would like an updated one.")
        continue
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"Image for {county} has been saved successfully at {output_path}!")
    else:
        print(f"Failed to retrieve image for {county}. Status code: {response.status_code}")