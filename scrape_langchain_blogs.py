import os
import re
import requests
import time
import random
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Base URL and output directory
base_url = "https://blog.langchain.dev"
output_dir = "langchain_blogs/in_the_loop"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Configure retry strategy
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

# Fetch the main page
response = session.get(f"{base_url}/tag/in-the-loop/")
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all blog post URLs
blog_links = []
for article in soup.find_all('article'):
    link_element = article.find('a', href=True)
    if link_element:
        href = link_element['href']
        if href.startswith('/'):
            full_url = base_url + href
            blog_links.append(full_url)

print(f"Found {len(blog_links)} blog posts to scrape")

# Scrape each blog post
for i, url in enumerate(blog_links):
    print(f"Scraping {i+1}/{len(blog_links)}: {url}")

    # Check if file already exists (to resume interrupted scraping)
    # Extract a temporary title from URL for checking
    temp_title = url.split('/')[-2]
    temp_safe_title = re.sub(r'[^\w\s-]', '', temp_title).strip().replace('-', '_')
    temp_filepath = os.path.join(output_dir, f"{temp_safe_title}.md")

    if os.path.exists(temp_filepath):
        print(f"File already exists, skipping: {temp_filepath}")
        continue

    try:
        # Fetch the blog post with retry logic
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title_element = soup.find('h1')
        if title_element:
            title = title_element.text.strip()
        else:
            title = f"Article_{i+1}"

        # Create a safe filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        filename = f"{safe_title}.md"
        filepath = os.path.join(output_dir, filename)

        # Extract the main content
        content_element = soup.find('article')
        if content_element:
            # Convert to markdown
            markdown_content = md(str(content_element), heading_style="ATX")

            # Add title and URL at the top
            full_content = f"# {title}\n\nOriginal URL: {url}\n\n{markdown_content}"

            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            print(f"Saved to {filepath}")
        else:
            print(f"Could not find content for {url}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

    # Be nice to the server - random delay between 2-5 seconds
    delay = 2 + random.random() * 3
    print(f"Waiting {delay:.2f} seconds before next request...")
    time.sleep(delay)

print("Scraping completed!")
