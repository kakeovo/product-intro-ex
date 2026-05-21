import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_metadata(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.content, 'html.parser')

        metadata = {
            'title': None,
            'description': None,
            'image_url': None,
            'category': 'uncategorized'
        }

        # OGP tags
        og_title = soup.find('meta', property='og:title')
        if og_title:
            metadata['title'] = og_title.get('content')

        og_description = soup.find('meta', property='og:description')
        if og_description:
            metadata['description'] = og_description.get('content')

        og_image = soup.find('meta', property='og:image')
        if og_image:
            metadata['image_url'] = og_image.get('content')

        # Fallback: regular meta tags
        if not metadata['title']:
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.string

        if not metadata['description']:
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                metadata['description'] = desc_tag.get('content')

        return metadata

    except Exception as e:
        logger.error(f"Error extracting metadata from {url}: {e}")
        return {'title': url, 'description': None, 'image_url': None}
