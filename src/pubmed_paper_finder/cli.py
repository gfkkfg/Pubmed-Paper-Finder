import argparse
import sys
from pubmed_paper_finder.fetcher import (
    search_pubmed_ids,
    fetch_paper_details,
    filter_non_academic_authors,
    save_results_to_csv
)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers and extract non-academic authors from pharma/biotech companies."
    )

    parser.add_argument(
        "--query", "-q", type=str, required=True,
        help="Search query to fetch PubMed papers"
    )
    parser.add_argument(
        "--file", "-f", type=str,
        help="Optional: Save output to CSV file"
    )
    parser.add_argument(
        "--debug", "-d", action="store_true",
        help="Print debug info while processing"
    )

    args = parser.parse_args()

    if args.debug:
        print(f"Query: {args.query}")
        print("Searching PubMed...")

    ids = search_pubmed_ids(args.query, max_results=20)
    if args.debug:
        print(f"Found {len(ids)} papers")

    papers = fetch_paper_details(ids)
    if args.debug:
        print(f"Retrieved metadata for {len(papers)} papers")

    filtered = filter_non_academic_authors(papers)
    if args.debug:
        print(f"Found {len(filtered)} papers with non-academic authors")

    if args.file:
        save_results_to_csv(filtered, args.file)
        print(f"Results saved to {args.file}")
    else:
        for paper in filtered:
            print(f"\n{paper['Title']}")
            print(f"PubMed ID: {paper['PubmedID']}")
            print(f"Published: {paper['PublicationDate']}")
            print(f"Non-academic Authors: {', '.join(paper['NonAcademicAuthors'])}")
            print(f"Affiliations: {', '.join(paper['CompanyAffiliations'])}")

if __name__ == "__main__":
    main()
