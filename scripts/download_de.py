import re
import urllib.request
import urllib.error
import ssl
import holmes_extractor as holmes
from wasabi import Printer
import typer
from pathlib import Path
from bs4 import BeautifulSoup

"""This script downloads and saves Harry Potter Chapters for the english literature example (Topic Matching)"""

msg = Printer()

def main(model_name:str, working_dir:Path):

    msg.info("Initializing Holmes")
    holmes_manager = holmes.Manager(
        model=model_name)
    msg.good("Holmes initialized")

    def extract_DE_literature(front_page_uri, front_page_label):
        """ Download and save all the stories from a front page."""
        try:
            msg.info(f"Request to {front_page_uri}")
            front_page = urllib.request.urlopen(front_page_uri)
        except (ssl.SSLCertVerificationError, urllib.error.URLError) as e:
            msg.fail("SSLCertVerificationError/urllib.error.URLError")
            msg.info(f"Restarting request to {front_page_uri} with ssl._create_unverified_context")
            ssl._create_default_https_context = ssl._create_unverified_context
            front_page = urllib.request.urlopen(front_page_uri)

        msg.good("Successful request")

        front_page_soup = BeautifulSoup(front_page, 'html.parser')
        document_texts = []
        labels = []
        # For each story ...
        for anchor in front_page_soup.find_all('a'):
            if not anchor['href'].startswith('/') and not anchor['href'].startswith('https'):
                this_document_url = '/'.join((front_page_uri, anchor['href']))
                msg.info('Downloading story', anchor.contents[0], 'from front page', front_page_label)
                # Get the HTML document for the story
                this_document = urllib.request.urlopen(this_document_url)
                # Extract the raw text from the HTML document
                this_document_soup = BeautifulSoup(this_document, 'html.parser')
                this_document_text = this_document_soup.prettify()
                this_document_text = this_document_text.split('</h1>', 1)[1]
                this_document_text = this_document_text.split('<span class="autor"', 1)[0]
                this_document_text = this_document_text.replace('<br/>', ' ')
                # Remove any carriage returns and line feeds from the raw text
                this_document_text = this_document_text.replace(
                    '\n', ' ').replace('\r', ' ').replace('  ', ' ')
                # Replace multiple spaces with single spaces
                this_document_text = ' '.join(this_document_text.split())
                # Create a document label from the front page label and the story name
                this_document_label = ' - '.join((front_page_label, anchor.contents[0]))
                document_texts.append(this_document_text)
                labels.append(this_document_label)
        parsed_documents = holmes_manager.nlp.pipe(document_texts)
        for index, parsed_document in enumerate(parsed_documents):
            label = labels[index] + ".hdc"
            print('Saving', label)
            output_filename = working_dir / label
            with open(output_filename, "wb") as file:
                file.write(parsed_document.to_bytes())

    extract_DE_literature("https://maerchen.com/grimm/", 'Gebrüder Grimm')
    extract_DE_literature("https://maerchen.com/grimm2/", 'Gebrüder Grimm')
    extract_DE_literature("https://maerchen.com/andersen/", 'Hans Christian Andersen')
    extract_DE_literature("https://maerchen.com/bechstein/", 'Ludwig Bechstein')
    extract_DE_literature("https://maerchen.com/wolf/", 'Johann Wilhelm Wolf')

if __name__ == "__main__":
    typer.run(main)