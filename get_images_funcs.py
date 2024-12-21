from bs4 import BeautifulSoup
import requests

def get_image_urls_via_scraping(urls: list, updated_counties: list) -> dict:
    # Get image URLs from wikipedia
    img_urls = {}

    for i, url in enumerate(urls):   
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", class_="infobox ib-settlement vcard")
        img_urls[updated_counties[i]] = None
        if table:
            infobox_cells = table.find_all("td", class_="infobox-full-data")
            if len(infobox_cells) > 1:
                j = 1 # start at 1 to skip the first cell which doesn't contain the map
                while j < len(infobox_cells):
                    img_tag = infobox_cells[j].find("img")
                    if img_tag and "src" in img_tag.attrs and ('map' in img_tag["src"].lower() or '.svg.png' in img_tag["src"].lower()):  # Greater London doesn't have map in its map URL
                        img_url = img_tag["src"]
                        if not img_url.startswith("http"):
                            img_url = "https:" + img_url
                        img_urls[updated_counties[i]] = img_url.replace("250", "500")
                        break
                    j += 1
                if img_urls[updated_counties[i]] is None:
                    print(f"No image found for {updated_counties[i]}")   
            else:
                print(f"Only {len(infobox_cells)} cells found at {url}")
        else:
            print(f"No table found at {url}")
    return img_urls

def get_image_urls_via_api(page_title: str) -> tuple[list[str], list[str]]:
    api_url = "https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    params = {"action": "query", "titles": page_title, "prop": "images", "format": "json"}
    
    image_filenames = []

    while True:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        # print(data)
    
        # Extract image filenames
        page_id = list(data["query"]["pages"].keys())[0]
        if "images" not in data["query"]["pages"][page_id]:
            print("No images found on the page.")
            return []
        images = data["query"]["pages"][page_id]["images"]
        image_filenames.extend([image["title"] for image in images])

        # Check if there are more images to fetch
        if "continue" in data:
            for k, v in data["continue"].items():
                if k != "continue":
                    params[k] = v
           # print(data["continue"])
        else:
            break

    # Fetch the URLs for the images
    image_urls = []
    for filename in image_filenames:
        params = {
            "action": "query",
            "titles": filename,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json"
        }
        response = requests.get(api_url, params=params, headers=headers)
        image_data = response.json()
        image_page_id = list(image_data["query"]["pages"].keys())[0]
        if "imageinfo" in image_data["query"]["pages"][image_page_id]:
            image_url = image_data["query"]["pages"][image_page_id]["imageinfo"][0]["url"]
            image_urls.append(image_url)
    
    return image_filenames, image_urls