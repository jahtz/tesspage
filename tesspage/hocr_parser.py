from pathlib import Path
from datetime import datetime

from bs4 import BeautifulSoup

from tesspage.document import Document, Page, TextRegion, TextLine, page_to_string


class HOCRParser:
    def __init__(self, path: Path):
        self.fp = path
        self.document: Document = self.__parse(self.__check_valid())

    def __check_valid(self) -> BeautifulSoup:
        """
        Check for valid HOCR file

        Returns:
            BeautifulSoup object
        """
        with open(self.fp.as_posix(), 'r', encoding='utf-8') as f:
            data = f.read()
        return BeautifulSoup(data, 'html.parser')

    def __parse(self, bs: BeautifulSoup) -> Document:
        """
        Parsing BeautifulSoup object to Document object

        Args:
            bs: BeautifulSoup object

        Returns:
            Document object
        """
        doc = Document(file=self.fp.as_posix(), id=self.fp.name.replace('hocr', ''))

        creator = bs.find('meta', {'name': 'ocr-system'})
        if creator is not None:
            doc.creator = creator['content']

        doc.created = str(datetime.utcnow().isoformat(timespec="seconds"))  # maybe change to actual creation time
        doc.last_change = str(datetime.utcnow().isoformat(timespec="seconds"))

        for page in bs.find_all('div', {'class': 'ocr_page'}):
            p_data = self.__data_parser(page['title'])
            p = Page(
                id=page['id'],
                file=p_data['image'],
                height=p_data['bbox'][2][1],
                width=p_data['bbox'][2][0],
            )
            for region in page.find_all('div', {'class': 'ocr_carea'}):
                try:
                    r_data = self.__data_parser(region['title'])
                    r = TextRegion(
                        id=region['id'],
                        coords=r_data['bbox'],
                    )
                    for line in region.find_all('span', {'class': 'ocr_line'}):
                        try:
                            l_data = self.__data_parser(line['title'])
                            l = TextLine(
                                id=line['id'],
                                text=' '.join([x.text for x in line.find_all('span', {'class': 'ocrx_word'})]),
                                coords=l_data['bbox'],
                            )
                            r.text_lines.append(l)
                        except AttributeError:
                            print(f'\tError in TextLine: {line["id"]}')
                            continue  # ignore line on missing data
                    p.text_regions.append(r)
                except AttributeError:
                    print(f'\tError in TextRegion: {region["id"]}')
                    continue  # ignore region on missing data
            doc.pages.append(p)
        return doc

    def __data_parser(self, data: str) -> dict:
        """
        Parsing HOCR title data to dictionary

        Args:
            data: data from 'title' argument

        Returns:
            formatted data
        """
        form = {}
        for i in data.split('; '):
            d = i.split(' ', 1)
            if d[0] == 'bbox':
                c = d[1].split(' ')
                form[d[0]] = [[c[0], c[1]], [c[2], c[1]], [c[2], c[3]], [c[0], c[3]]]
            elif d[0] == 'image':
                form[d[0]] = d[1].replace('"', '')
            else:
                form[d[0]] = d[1]
        return form


def parse_hocr(path: Path) -> Document:
    """
    Parse HOCR file to Document object

    Args:
        path: absolute .hocr file path

    Returns:
        Document object
    """
    return HOCRParser(path).document


def hocr_to_string(path: Path) -> str:
    """
    Parsing PageXML file to single string

    Args:
        path: path to PageXML file

    Returns:
        formatted string (separators for page \\n\\n\\n, regions \\n\\n, lines \\n)

    """
    doc = parse_hocr(path)
    return '\n\n\n'.join([page_to_string(page) for page in doc.pages])
