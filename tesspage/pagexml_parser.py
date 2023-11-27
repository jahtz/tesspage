from pathlib import Path

from bs4 import BeautifulSoup

from tesspage.document import Document, Page, TextRegion, TextLine, page_to_string


class PageXMLParser:
    def __init__(self, path: Path):
        self.fp = path
        self.document: Document = self.__parse(self.__check_valid())

    def __check_valid(self) -> BeautifulSoup:
        """
        Check for valid PageXML formatting

        :return: BeautifulSoup object of xml file
        """
        if not self.fp.exists():
            raise FileNotFoundError(self.fp.as_posix() + 'does not exist!')
        if not self.fp.is_file():
            raise IsADirectoryError(self.fp.as_posix() + 'is a directory!')
        if not self.fp.suffix != 'xml':
            raise TypeError(self.fp.as_posix() + 'is no .xml file!')

        with open(self.fp.as_posix(), 'r', encoding='utf-8') as f:
            data = f.read()
        bs = BeautifulSoup(data, 'xml')

        xml_data = bs.find('PcGts')
        if not (xml_data
                and ('xmlns' in xml_data.attrs)
                and ('http://schema.primaresearch.org/PAGE/gts/pagecontent/' in xml_data.attrs.get('xmlns'))
                ):  # check if file uses page scheme
            raise TypeError(self.fp.as_posix() + 'is not a PageXML file!')
        return bs

    def __parse(self, bs: BeautifulSoup) -> Document:
        """
        Parsing BeautifulSoup object to Document object

        Args:
            bs: BeautifulSoup object

        Returns:
            Documents object
        """
        doc = Document(file=self.fp.as_posix(), id=self.fp.name.replace('.xml', ''))
        meta = bs.find('Metadata')

        creator = meta.find('Creator')
        if creator is not None:
            doc.creator = creator.text

        created = meta.find('Created')
        if created is not None:
            doc.created = created.text

        last_change = meta.find('LastChange')
        if last_change is not None:
            doc.last_change = last_change.text

        page_counter = 0
        for page in bs.find_all('Page'):
            p = Page(
                id=f'page_{page_counter}',
                file=self.fp.parent.joinpath(page.attrs.get('imageFilename')).as_posix(),
                height=int(page.attrs.get('imageHeight')),
                width=int(page.attrs.get('imageWidth'))
            )
            for region in page.find_all('TextRegion'):
                try:
                    r = TextRegion(
                        id=region.attrs.get('id'),
                        coords=[[int(x) for x in y.split(',')] for y in
                                region.find('Coords').attrs.get('points').split(' ')]
                    )
                    for line in region.find_all('TextLine'):
                        try:
                            l = TextLine(
                                id=line.attrs.get('id'),
                                text=line.find('Unicode').text,
                                coords=[[int(x) for x in tuples.split(',')] for tuples in
                                        line.find('Coords').attrs.get('points').split(' ')],
                            )
                            r.text_lines.append(l)
                        except AttributeError:
                            print(f'\tError in TextLine: {line.attrs.get("id")}')
                            continue  # ignore line on missing data
                    p.text_regions.append(r)
                except AttributeError:
                    print(f'\tError in TextRegion: {region.attrs.get("id")}')
                    continue  # ignore region on missing data
            doc.pages.append(p)
            page_counter += 1
        return doc


def parse_pagexml(path: Path) -> Document:
    """
    Parse PageXML file to Document object

    Args:
        path: path to pagexml file

    Returns:
        Document object
    """
    return PageXMLParser(path).document


def pagexml_to_string(path: Path) -> str:
    """
    Parsing PageXML file to single string

    Args:
        path: path to PageXML file

    Returns:
        formatted string (separators for page \\n\\n\\n, regions \\n\\n, lines \\n)

    """
    doc = parse_pagexml(path)
    return '\n\n\n'.join([page_to_string(page) for page in doc.pages])
