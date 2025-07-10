from typing import List
from Bio import Entrez
from typing import Dict
import csv

Entrez.email = "thangarajsankar620@gmail.com" 

def search_pubmed_ids(query: str, max_results: int = 10) -> List[str]:
    """
    Search PubMed for paper IDs based on the user query.

    Args:
        query (str): Search keyword (e.g., "diabetes treatment").
        max_results (int): Maximum number of papers to fetch.

    Returns:
        List[str]: List of PubMed IDs matching the query.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """
    Get detailed paper info from a list of PubMed IDs.
    
    Args:
        pubmed_ids (List[str]): List of PubMed paper IDs.
    
    Returns:
        List[Dict]: List of paper metadata.
    """
    ids_str = ",".join(pubmed_ids)
    handle = Entrez.efetch(db="pubmed", id=ids_str, rettype="medline", retmode="xml")
    records = Entrez.read(handle)

    papers = []
    for article in records["PubmedArticle"]:
        info = {}
        medline = article["MedlineCitation"]
        article_data = medline["Article"]

        info["PubmedID"] = str(medline.get("PMID", "?"))
        info["Title"] = article_data.get("ArticleTitle", "No title")

        # Try to get publication year
        pub_date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        info["PublicationDate"] = pub_date.get("Year") or pub_date.get("MedlineDate") or "Unknown"

        authors = article_data.get("AuthorList", [])
        info["Authors"] = []
        info["Affiliations"] = []

        for author in authors:
            name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
            affils = author.get("AffiliationInfo", [])
            for affil in affils:
                info["Authors"].append(name)
                info["Affiliations"].append(affil.get("Affiliation", ""))

        papers.append(info)

    return papers

def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """
    Filters out non-academic authors and company affiliations from paper details.
    
    Arts:
        papers (list[Dict]): List of full paper data.
        
    Returns:
        List[Dict]: List of filtered records with non-academic authors and companies.
    """
    academic_keywords = ['university', 'college', 'hospital', 'school', 'institute', 'dept', 'department', 'faculty', 'center', 'centre', 'lab']

    filtered_results = []

    for paper in papers:
        non_academic_authors = []
        company_affiliations = []

        for author, affiliation in zip(paper["Authors"], paper["Affiliations"]):
            affil_lower = affiliation.lower()
            if not any(keyword in affil_lower for keyword in academic_keywords):
                non_academic_authors.append(author)
                company_affiliations.append(affiliation)

        if non_academic_authors:
            filtered_results.append({
                "PubmedID": paper["PubmedID"],
                "Title": paper["Title"],
                "PublicationDate": paper["PublicationDate"],
                "NonAcademicAuthors": non_academic_authors,
                "CompanyAffiliations": company_affiliations,
            })
        
    return filtered_results

def save_results_to_csv(results: List[Dict], filename: str):
    """
    Save filtered paper data to a CSV file.
    
    Args:
        results (List[Dict]): Filtered papers.
        filename (str): Path to output CSV.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-Academic Authors",
            "Company Affiliations"
        ])
        for r in results:
            writer.writerow([
                r["PubmedID"],
                r["Title"],
                r["PublicationDate"],
                "; ".join(r["NonAcademicAuthors"]),
                "; ".join(r["CompanyAffiliations"]),
            ])