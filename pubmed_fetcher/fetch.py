import requests
from typing import List

def fetch_pubmed_ids(query: str, retmax: int = 50) -> List[str]:
    """
    Fetch PubMed IDs for a given query using NCBI E-utilities.
    
    Args:
        query (str): PubMed search query.
        retmax (int): Maximum number of results to return.

    Returns:
        List[str]: List of PubMed ID strings.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]
 
