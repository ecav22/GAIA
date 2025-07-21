import requests
import pandas as pd

def scrape_ifc_disclosures(query="climate", page_size=100):
    base_url = "https://disclosures.ifc.org/api/v1/projects"
    headers = {
        "Accept": "application/json"
    }
    projects = []
    offset = 0

    while True:
        params = {
            "keyword": query,
            "offset": offset,
            "limit": page_size
        }
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            break
        data = response.json()
        results = data.get("projects", [])
        if not results:
            break

        for proj in results:
            projects.append({
                "Project ID": proj.get("projectId"),
                "Title": proj.get("title"),
                "Region": proj.get("region"),
                "Country": proj.get("country"),
                "Sector": proj.get("sector"),
                "Disclosure Date": proj.get("disclosureDate"),
                "URL": f"https://disclosures.ifc.org/project-detail/{proj.get('projectId')}"
            })
        offset += page_size

    df = pd.DataFrame(projects)
    df.to_csv("ifc_disclosures.csv", index=False)
    return df

# Example run
if __name__ == "__main__":
    df = scrape_ifc_disclosures("climate")
    print(df.head())
