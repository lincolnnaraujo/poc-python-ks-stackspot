import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

import html2text
import requests
from bs4 import BeautifulSoup


def url_to_markdown(base_url, output_dir):
    """
    Save all child links of a webpage as UTF-8 encoded markdown files.
    """
    results = {
        'success': 0,
        'errors': 0,
        'saved_files': []
    }

    # Initialize HTML to Markdown converter with UTF-8 support
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    h.unicode_snob = True

    try:
        # Get the base page content with UTF-8 encoding
        response = requests.get(base_url)
        response.encoding = 'utf-8'
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links in the page
        links = soup.find_all('a', href=True)

        # Convert to absolute URLs and remove duplicates
        unique_links = set()
        for link in links:
            absolute_url = urljoin(base_url, link['href'])
            if absolute_url.startswith('http') and '#' not in absolute_url:
                unique_links.add(absolute_url)

        total_links = len(unique_links)
        print(f"Encontrados {total_links} links únicos para processar.")

        # Process each link
        for i, url in enumerate(unique_links, 1):
            try:
                # Update progress
                progress_percent = int((i / total_links) * 100)

                # Get the page content
                page_response = requests.get(url)
                page_response.encoding = 'utf-8'
                page_response.raise_for_status()

                # Parse the HTML
                page_soup = BeautifulSoup(page_response.text, 'html.parser')

                # Remove unwanted elements
                for element in page_soup(['script', 'style', 'nav', 'footer', 'iframe']):
                    element.decompose()

                # Get the main content
                main_content = page_soup.find('article') or page_soup.find('main') or page_soup.find(
                    'body') or page_soup

                # Convert HTML to Markdown
                markdown_content = h.handle(str(main_content))

                # Create filename
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.replace('www.', '').split('.')[0]
                path = parsed_url.path.strip('/').replace('/', '_') or 'index'

                #Formatar nomes de arquivos
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # Formato: AAAAMMDDHHMMSSmmmmmm
                max_length = 50
                base_filename = f"{domain}_{path}"
                remaining_length = max_length - len(timestamp) - 1  # Subtraia o tamanho do timestamp e o "_"
                truncated_base = base_filename[:remaining_length]  # Trunca o base_filename se necessário

                # Nome dos arquivos markdown
                filename = f"{truncated_base}_{timestamp}.md"
                filename = re.sub(r'[^\w\-.]', '', filename)[:50]
                filepath = os.path.join(output_dir, filename)

                # Save with UTF-8 encoding
                with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
                    f.write(f"# Source: {url}\n\n")
                    f.write(markdown_content)

                # Conceder permissões totais para o arquivo
                #os.chmod(filepath, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

                results['success'] += 1
                results['saved_files'].append(filepath)

            except Exception as e:
                results['errors'] += 1
                print(f"Erro processando {url}: {str(e)}")
                raise e

    except Exception as e:
        print(f"Erro processando URL base {base_url}: {str(e)}")
        raise e

    return results