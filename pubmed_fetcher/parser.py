import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    """
    Fetch detailed information about PubMed papers using EFetch.

    Args:
        paper_ids (List[str]): List of PubMed IDs.

    Returns:
        List[Dict]: List of paper metadata dictionaries.
    """
    if not paper_ids:
        return []

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        affiliations = article.findall(".//AffiliationInfo/Affiliation")

        authors = []
        companies = []
        emails = []

        for aff in affiliations:
            text = aff.text or ""
            if any(x in text.lower() for x in ["pharma", "biotech", "inc", "ltd", "company", "corporation"]):
                companies.append(text)

            if "@" in text:
                emails.append(text)

            if not any(x in text.lower() for x in ["university", "college", "institute", "hospital", "school"]):
                authors.append(text)

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(set(authors)) or "N/A",
            "Company Affiliation(s)": "; ".join(set(companies)) or "N/A",
            "Corresponding Author Email": emails[0] if emails else "N/A"
        })

    return papers
