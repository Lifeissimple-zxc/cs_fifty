import re
import logging

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import markdown2


logger = logging.getLogger('wiki')

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    
def fetch_entry(title: str):
    """Wrapper around get_entry that enables case agnostic searches

    Args:
        title (str): title to search
    """
    # assumption: most titles are capitalised, all upper is a fall back scenario
    if (markdown := get_entry(title=title.capitalize())) is not None:
        return markdown
    logger.warning("capitalised search did not work")
    return get_entry(title=title.upper())
    
def string_to_markdown(title:str, markdown: str) -> markdown2.UnicodeWithAttrs:
    try:
        return markdown2.markdown(text=markdown)
    except Exception as e:
        logger.error("error converting markdown for title %s: %s", title, e)

