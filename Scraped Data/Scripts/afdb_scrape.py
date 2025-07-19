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