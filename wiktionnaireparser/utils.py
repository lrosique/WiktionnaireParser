import re
import json
from contextlib import suppress
from lxml.html import HtmlComment


def etymology_cleaner(etymology):
    """
    Cleans up the etymology of the text prompting
    site visitors to contribute.
    """
    ignore_etym = [
        r'^Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici\.$',
        r'\(Siècle à préciser\) ',
    ]
    for ignore in ignore_etym:
        etymology = re.sub(ignore, '', etymology)
    return etymology


def filter_sections_id(sections, useless_sections):
    """Filters interesting sections."""
    filtered_sections = []
    for sections_ in sections:
        if any(re.search(x, sections_) for x in useless_sections):
            continue
        filtered_sections.append(sections_)
    return filtered_sections


def extract_related_words(section):
    """Extract related words."""
    related = {}
    count = 0
    while section is not None and section.tag != 'h3' and section.tag != 'h4':
        words = []
        description = ''
        if not type(section) is HtmlComment:
            if section.cssselect('.NavContent'):
                with suppress(IndexError):
                    description = section.cssselect('.NavHead')[0].text_content()
                for link in section.cssselect('.NavContent a'):
                    if 'Annexe:' in link.attrib.get('href'):
                        continue
                    words.append(link.text_content())

            else:
                for link in section.cssselect('a'):
                    if 'Annexe:' in link.attrib.get('href'):
                        continue
                    words.append(link.text_content())
            related[count] = {}
            related[count]['description'] = description
            related[count]['words'] = words
        section = section.getnext()
        count += 1
    return related

def get_language_name(lang_code):
    """Get language name from languge code."""
    with open('wiktionnaireparser/languages.json', 'r') as f:
        languages_json = json.loads(f.read())
    try:
        return languages_json[lang_code]
    except KeyError:
        raise KeyError('Language code unknown : %s' % lang_code)
