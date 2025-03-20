import requests
import os
import time

def get_chapter_data(chapter_id):
    """ Fetches chapter data, including the next chapter's sequence """
    
    api_url = f"https://example.com/api/chapter/{chapter_id}"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Error accessing API ({response.status_code})")
        return None, None

    data = response.json().get("data", {})
    attributes = data.get("attributes", {})
    
    manga_id = data.get("manga_id", None)
    chapter_number = attributes.get("chapter", "0")

    return manga_id, chapter_number


def get_next_chapter(manga_id, current_chapter):
    """ Finds the next chapter via API """
    
    api_url = f"https://example.com/api/chapters"
    params = {
        "manga": manga_id,
        "language": "en",  # Change as needed
        "order": "asc",
        "limit": 100
    }
    
    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        print(f"Error fetching next chapter ({response.status_code})")
        return None

    chapters = response.json().get("data", [])

    found = False
    for chapter in chapters:
        chapter_num = chapter.get("chapter", "0")

        if found:
            return chapter["id"]

        if chapter_num == current_chapter:
            found = True

    return None


def get_image_links(chapter_id):
    """ Fetches image links for the chapter """
    
    api_url = f"https://example.com/api/chapter/{chapter_id}/images"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Error accessing image API ({response.status_code})")
        return []

    data = response.json()
    base_url = data["baseUrl"]
    image_paths = data["images"]

    return [f"{base_url}/{img}" for img in image_paths]


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

# Start from this initial chapter ID (replace with your own ID)
chapter_id = "your-chapter-id-here"
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

    manga_id, chapter_number = get_chapter_data(chapter_id)
    if not manga_id:
        print("No next chapter found. Download complete!")
        break

    next_chapter_id = get_next_chapter(manga_id, chapter_number)
    if not next_chapter_id:
        print("No next chapter found. Download complete!")
        break

    chapter_id = next_chapter_id
    chapter_number += 1

    time.sleep(1)  # Avoid overwhelming the server
