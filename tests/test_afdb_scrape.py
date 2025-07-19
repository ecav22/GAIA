import importlib.util
from pathlib import Path

# Load the module from its file location because the directory name contains a space
module_path = Path(__file__).resolve().parents[1] / 'Scraped Data' / 'Scripts' / 'afdb_scrape.py'
spec = importlib.util.spec_from_file_location('afdb_scrape', module_path)
afdb_scrape = importlib.util.module_from_spec(spec)
spec.loader.exec_module(afdb_scrape)


def test_parse_links_basic():
    html = """
    <html>
        <body>
            <a href=\"/doc1\">Document 1</a>
            <a href=\"https://example.com/doc2\">Doc2</a>
        </body>
    </html>
    """
    assert afdb_scrape.parse_links(html) == ["/doc1", "https://example.com/doc2"]

