"""
A script that does the following post-processing steps
on the Discord channel dump found in the `original_html`
subdirectory:

1. Parse each HTML file to find all image URLs, including
   embedded images, attachments, and emojis.
2. Download each image from Discord's CDN and save it
   into a local `assets` directory.
3. Update the HTML files to point to the locally saved
   images instead of the original URLs.
4. Save the updated HTML files into the root directory
   (thus preserving the original files in `original_html`).

Created by Nicholas H.Tollervey.

Copyright © `2025` `Anaconda Inc.`

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path

# Directory containing the original HTML files
ORIGINAL_HTML_DIR = Path("original_html")
# Directory to save downloaded assets
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)


def download_image(url, save_path):
    """
    Download an image from a URL and save it to the specified path.
    """
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(response.content)


def process_html_file(html_file_path):
    """
    Process a single HTML file: download images and update URLs.
    """
    with open(html_file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all image tags
    img_tags = soup.find_all("img")
    for img in img_tags:
        src = img.get("src")
        if src and "cdn.discordapp.com" in src:
            # Parse the URL to get the filename
            parsed_url = urlparse(src)
            filename = os.path.basename(parsed_url.path)
            local_path = ASSETS_DIR / filename

            # Download the image if not already downloaded
            if not local_path.exists():
                print(f"Downloading {src} to {local_path}")
                download_image(src, local_path)

            # Update the img tag to point to the local asset
            img["src"] = str(local_path)

    # Save the updated HTML file to the root directory
    updated_html_path = Path(html_file_path.name)
    with open(updated_html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Updated HTML saved to {updated_html_path}")


def main():
    """
    Main function to process all HTML files in the original_html directory.
    """
    for html_file in ORIGINAL_HTML_DIR.glob("*.html"):
        print(f"Processing {html_file}")
        process_html_file(html_file)


if __name__ == "__main__":
    main()
