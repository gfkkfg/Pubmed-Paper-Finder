PubMed Paper Finder

A Python command-line tool to fetch PubMed research papers and extract non-academic authors from pharmaceutical or biotech companies.

---

## Features

- Search PubMed using any keyword (supports advanced PubMed queries).
- Fetch paper metadata: title, authors, affiliations, date.
- Identify non-academic authors based on affiliation heuristics.
- Export results to CSV (optional).
- Fully configurable from the command line.
- Packaged using Poetry.

---

## Project Structure

pubmed-paper-finder/
| -- pubmed_paper_finder/
| | -- fetcher.py # Core logic: fetch, filter, save
| | -- cli.py # Command-line interface
| -- pyproject.toml # Poetry config and script entry
| -- README.md # Project documentation

---

## How to Install & Run

### Install Poetry (if not already):

curl -sSL https://install.python-poetry.org | python3 -

### Clone and Install:

git clone https://github.com/gfkkfg/Pubmed-Paper-Finder.git

cd Pubmed-Paper-Finder

poetry install

## Run it:

poetry run get-papers-list --query "cancer treatment"

## Optional flags:

--file results.csv  # Save results to a CSV
--debug             # Show extra output
-h or --help        # See usage guide

## Example Usage

poetry run get-papers-list --query "diabetes therapy" --file diabetes.csv

## Tools & Libraries Used
- BioPython - PubMed API access
- Poetry - Dependency management
- argparse - Command-line interface

### Author:
- Built by Thangaraj M
- Linkedin: https://www.linkedin.com/in/thangarajsankar
- Portfolio: https://thangaraj.onrender.com