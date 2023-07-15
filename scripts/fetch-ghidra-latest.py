import sys
import requests
from bs4 import BeautifulSoup

URL = 'https://github.com/NationalSecurityAgency/ghidra/releases/latest'
GHIDRA_DEST = '/tmp/ghidra.zip'

def main():
    needle = 'expanded_assets'
    r = requests.get(
        url=URL,
        allow_redirects=True
    )
    html_source = r.text
    soup = BeautifulSoup(html_source, 'html.parser')
    
    fragments = soup.find_all('include-fragment')
    if len(fragments) == 0:
        return False
    
    url = fragments[2].get('src', None)
    if url is None:
        return False
    
    r = requests.get(
        url=url,
        allow_redirects=True
    )

    html_source = r.text
    soup = BeautifulSoup(html_source, 'html.parser')

    hrefs = soup.find_all('a')
    url = 'https://github.com' + hrefs[0].get('href', None)
    
    with open(GHIDRA_DEST, 'wb') as f:
        r = requests.get(url, allow_redirects=True, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return True

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)