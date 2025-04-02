import requests
import os
import time

def get_chapter_data(chapter_id):
    """ Fetches chapter data, including the next chapter's sequence """
    
    api_url = f"https://api.mangadex.org/chapter/{chapter_id}"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Error accessing API ({response.status_code})")
        return None, None

    data = response.json().get("data", {})
    attributes = data.get("attributes", {})
    
    manga_id = next((rel["id"] for rel in data.get("relationships", []) if rel["type"] == "manga"), None)
    chapter_number = attributes.get("chapter", "0")

    return manga_id, int(chapter_number) if chapter_number.isdigit() else 0

def get_next_chapter(manga_id, current_chapter_id):
    """ Finds the next chapter via API """
    
    api_url = "https://api.mangadex.org/chapter"
    params = {
        "manga": manga_id,
        "translatedLanguage[]": ["en"],  # Fetch only English chapters
        "order[createdAt]": "asc",  # Sort by creation date (ascending)
        "limit": 100
    }
    
    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        print(f"Error fetching next chapter ({response.status_code})")
        return None

    chapters = response.json().get("data", [])

    # Find the current chapter in the ordered list and return the next one
    for i, chapter in enumerate(chapters):
        if chapter["id"] == current_chapter_id and i + 1 < len(chapters):
            return chapters[i + 1]["id"]

    return None

def get_image_links(chapter_id):
    """ Fetches image links for the chapter """
    
    api_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Error accessing image API ({response.status_code})")
        return []

    data = response.json()
    base_url = data["baseUrl"]
    chapter_hash = data["chapter"]["hash"]
    images = data["chapter"]["data"]

    return [f"{base_url}/data/{chapter_hash}/{img}" for img in images]

def download_images(image_links, folder):
    """ Downloads chapter images and saves them in the specified folder """
    
    os.makedirs(folder, exist_ok=True)

    for i, img_url in enumerate(image_links):
        filename = f"{i+1:02d}.jpg"
        filepath = os.path.join(folder, filename)

        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Downloaded: {filename} ({folder})")
            else:
                print(f"Error downloading {img_url} (Status Code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")

#  Initial configuration
main_folder = "Downloaded_Manga"
os.makedirs(main_folder, exist_ok=True)

# Start from this initial chapter ID
chapter_id = "213255d-4rtrt-4rtrtr-9rtrtrtr"
chapter_number = 1

# Automatically download all chapters
while chapter_id:
    chapter_folder = os.path.join(main_folder, f"Chapter_{chapter_number:02d}")
    print(f"\n Downloading {chapter_folder}...")

    image_links = get_image_links(chapter_id)
    if image_links:
        download_images(image_links, chapter_folder)
    else:
        print(f"No images found for {chapter_id}")
        break

    manga_id, _ = get_chapter_data(chapter_id)
    if not manga_id:
        print("No next chapter found. Download complete!")
        break

    next_chapter_id = get_next_chapter(manga_id, chapter_id)
    if not next_chapter_id:
        print("No next chapter found. Download complete!")
        break

    chapter_id = next_chapter_id
    chapter_number += 1

    time.sleep(1)  # Avoid overwhelming the server