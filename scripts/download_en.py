import re
import urllib.request
import holmes_extractor as holmes
from wasabi import Printer
import typer
from pathlib import Path
from bs4 import BeautifulSoup

"""This script downloads and saves Harry Potter Chapters for the english literature example (Topic Matching)"""

msg = Printer()

def main(ontology_path:Path, model_name:str, working_dir:Path):
    msg.info('Initializing Ontology')
    ontology = holmes.Ontology(ontology_path)
    msg.good('Ontology initialized')

    msg.info("Initializing Holmes")
    holmes_manager = holmes.Manager(
        model=model_name, ontology=ontology)
    msg.good("Holmes initialized")

    def extract_chapters_from_book(book_uri, title):
        """ Download and save the chapters from a book."""
        msg.divider(f"Downloading {title}")
        book = urllib.request.urlopen(book_uri).read().decode()
        msg.good("Request successful")
        book = re.sub("\\nPage \|.+?Rowling \\n", "", book)
        book = re.sub("\\nP a g e \|.+?Rowling \\n", "", book)
        book = re.sub("\\nPage \|.+?\\n", "", book)
        book = book.replace("Harry Potter and the Half Blood Prince - J.K. Rowling", "")
        book = book.replace("Harry Potter and the Goblet of Fire - J.K. Rowling", "")
        book = book.replace("Harry Potter and the Deathly Hallows - J.K. Rowling", "")
        book = book[1:]
        chapter_headings = [heading for heading in re.finditer("(?<=((\\n\\n\\n\\n)|(\* \\n\\n)))((?!.*(WEASLEY WILL MAKE SURE)|(DO NOT OPEN THE PARCEL)|(HEADMISTRESS OF HOGWARTS))[A-Z][A-Z\-’., ]+)(\\n{1,2}((?!.*(WHO\-MUST))[A-Z\-’., ]+))?(?=(\\n\\n([^\\n]|(\\n\\n((“Harry!”)|(Harry’s)|(Ron’s)|(“Hagrid)|(Three o’clock))))))", book)]
        chapter_counter = 1
        labels = []
        chapter_texts = []
        chapter_dict = {}
        for chapter_heading in chapter_headings:
            label = ''.join((
                'Book ', title, ' Ch ', str(chapter_counter), " ‘",
                chapter_heading.group().replace('\n', '').strip(), "’"))
            labels.append(label)
            if chapter_counter == len(chapter_headings): # last chapter
                content = book[chapter_heading.end():]
            else:
                content = book[chapter_heading.end():chapter_headings[chapter_counter].start()]
            content = content.replace('\n', '')
            if content.endswith('& '):
                content = content[:-2]
            chapter_texts.append(content)
            msg.info('Extracted', label)
            chapter_counter += 1
        parsed_chapters = holmes_manager.nlp.pipe(chapter_texts)
        for index, parsed_chapter in enumerate(parsed_chapters):
            label = str(labels[index])+".hdc"
            msg.info('Saving', label)
            output_filename = working_dir / label
            
            with open(output_filename, "wb") as file:
                file.write(parsed_chapter.to_bytes())
            msg.good("Done")

    extract_chapters_from_book("https://raw.githubusercontent.com/formcept/whiteboard/master/nbviewer/notebooks/data/harrypotter/Book%201%20-%20The%20Philosopher's%20Stone.txt", "1 ‘The Philosopher\'s Stone’")
    extract_chapters_from_book("https://raw.githubusercontent.com/formcept/whiteboard/master/nbviewer/notebooks/data/harrypotter/Book%202%20-%20The%20Chamber%20of%20Secrets.txt", "2 ‘The Chamber of Secrets’")
    extract_chapters_from_book("https://raw.githubusercontent.com/formcept/whiteboard/master/nbviewer/notebooks/data/harrypotter/Book%203%20-%20The%20Prisoner%20of%20Azkaban.txt", "3 ‘The Prisoner of Azkaban’")
    extract_chapters_from_book("https://raw.githubusercontent.com/formcept/whiteboard/master/nbviewer/notebooks/data/harrypotter/Book%204%20-%20The%20Goblet%20of%20Fire.txt", "4 ‘The Goblet of Fire’")
    extract_chapters_from_book("https://raw.githubusercontent.com/formcept/whiteboard/master/nbviewer/notebooks/data/harrypotter/Book%205%20-%20The%20Order%20of%20the%20Phoenix.txt", "5 ‘The Order of the Phoenix’")
    extract_chapters_from_book("https://raw.githubusercontent.com/formcept/whiteboard/master/nbviewer/notebooks/data/harrypotter/Book%206%20-%20The%20Half%20Blood%20Prince.txt", "6 ‘The Half Blood Prince’")
    extract_chapters_from_book("https://raw.githubusercontent.com/formcept/whiteboard/master/nbviewer/notebooks/data/harrypotter/Book%207%20-%20The%20Deathly%20Hallows.txt", "7 ‘The Deathly Hallows’")

if __name__ == "__main__":
    typer.run(main)