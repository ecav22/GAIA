codex/add-tests-for-parse_links-function
"""Utility for scraping links from the AfDB projects page."""

from html.parser import HTMLParser


class _LinkParser(HTMLParser):
    """Simple HTML parser that collects href attributes."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.links.append(value)


def parse_links(html: str) -> list[str]:
    """Parse HTML and return a list of href values for all anchor tags."""
    parser = _LinkParser()
    parser.feed(html)
    return parser.links


def scrape_afdb_links() -> list[str]:
    """Use Selenium to fetch the AfDB projects page and return extracted links."""
    # Import Selenium locally so parse_links can be imported without the dependency
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 ...")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.afdb.org/en/documents/projects-operations")
        # Wait a bit for potential JavaScript/Cloudflare checks
        time.sleep(10)
        html = driver.page_source
    finally:
        driver.quit()

    return parse_links(html)


if __name__ == "__main__":
    for link in scrape_afdb_links():
        print(link)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def main():
    """Scrape AfDB documents page and return list of links."""
    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 ...")  # Optional

    driver = webdriver.Chrome(options=options)

    # Load the page
    driver.get("https://www.afdb.org/en/documents/projects-operations")

    # Let JavaScript load (Cloudflare check)
    time.sleep(10)  # Wait until Cloudflare passes

    # Extract page source
    html = driver.page_source

    # Parse page
    soup = BeautifulSoup(html, "html.parser")

    # Collect all links
    links = [a["href"] for a in soup.find_all("a", href=True)]

    driver.quit()
    return links


if __name__ == "__main__":
    main()
main
