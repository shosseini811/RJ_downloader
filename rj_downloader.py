import asyncio
import urllib.parse
from bs4 import BeautifulSoup
import re
import json
import requests
from requests_html import AsyncHTMLSession
import sys  # Import the sys module

# Check if a URL argument is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <URL>")
    sys.exit(1)

# Get the URL from the command-line arguments
url = sys.argv[1]

async def fetch_page():
    session = AsyncHTMLSession()

    response = await session.get(url)

    # Render the JavaScript
    await response.html.arender(wait=5, sleep=5)  # Wait for 5 seconds, then sleep for 5 seconds

    # Extract the HTML after JavaScript rendering
    html_content = response.html.html

    # Close the session
    await session.close()

    return html_content

async def main():
    # This will run the asynchronous function and retrieve the HTML content
    html_content = await fetch_page()

    # Parse the URL to extract the path
    url_path = urllib.parse.urlparse(url).path

    # Split the path by "/" and get the last part (song title)
    path_parts = url_path.split("/")
    song_title = path_parts[-1]

    # print("Song Title:", song_title)
    song_name = " ".join(song_title.split("-")[2:]).title()
    song_name

    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')
    matching_scripts = [script for script in script_tags if script.string and song_name in script.string]

    for script in matching_scripts:
        found_strings = script.find_all(string=re.compile(song_name, re.IGNORECASE))

        if found_strings:
            # Extract and print the output link if it exists
            link = None
            try:
                link = json.loads(found_strings[0])['props']['pageProps']['media']['link']
            except (ValueError, KeyError):
                pass

            if link:
                print("Output Link:", link)

    response = requests.get(link, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Specify the local path where you want to save the file
        with open(f"{song_name}.mp3", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print("Failed to download the file.")

if __name__ == "__main__":
    asyncio.run(main())
