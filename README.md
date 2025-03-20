# Manga Downloader
This script allows you to download manga chapters as image files from an API. You can configure it to automatically fetch and download sequential chapters.

## Features
- Fetch chapter data from an API.
- Automatically detect and download the next chapter.
- Save manga images in organized folders.

## Requirements
Make sure you have Python installed and install the required dependencies:
```sh
pip install requests
```
## Usage
1. Replace `your-chapter-id-here` with the starting chapter ID.
2. Run the script:
```sh
python script.py
```
3. The manga images will be downloaded into the `Downloaded_Manga` folder.

## Notes
- Ensure the API URL is correctly configured in the script.
- The script waits 1 second between requests to avoid overwhelming the server.

Enjoy your manga downloads! 🌸✨

