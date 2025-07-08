import click
from pubmed_fetcher.fetch import fetch_pubmed_ids
from pubmed_fetcher.parser import fetch_paper_details
import csv

@click.command()
@click.option('--query', '-q', required=True, help='PubMed query string')
@click.option('--file', '-f', default='', help='Output CSV filename (default: print to console)')
@click.option('--debug', '-d', is_flag=True, help='Enable debug output')
def main(query, file, debug):
    if debug:
        click.echo(f"Running query: {query}")

    paper_ids = fetch_pubmed_ids(query)
    click.echo(f"Found {len(paper_ids)} papers.")

    if not paper_ids:
        click.echo("No paper IDs returned.")
        return

    paper_data = fetch_paper_details(paper_ids)

    if not paper_data:
        click.echo("No metadata retrieved.")
        return

    if file:
        with open(file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=paper_data[0].keys())
            writer.writeheader()
            writer.writerows(paper_data)
        click.echo(f"Saved to {file}")
    else:
        for paper in paper_data:
            click.echo(paper)

if __name__ == '__main__':
    main()
