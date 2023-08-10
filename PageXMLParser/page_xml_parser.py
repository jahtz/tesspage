from bs4 import BeautifulSoup
from PageXMLParser.structure import PageXML, Page, Line
import pathlib
import numpy


def check_valid_page_xml(path: str):
    """Checks path for valid PageXML file

    Args:
        path: file path string

    Returns:
        BeautifulSoup4 object on valid file or raises error
    """
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f'{path} does not exist!')
    if not pathlib.Path(path).is_file():
        raise IsADirectoryError(f'{path} is a directory!')
    if not pathlib.Path(path).suffix != 'xml':
        raise TypeError(f'{path} is no .xml file!')

    bs = page_xml_to_bs4(path)
    xml_data = bs.find('PcGts')
    if not (xml_data
            and ('xmlns' in xml_data.attrs)
            and ('http://schema.primaresearch.org/PAGE/gts/pagecontent/' in xml_data.attrs.get('xmlns'))
            ):  # check if file uses page scheme
        raise TypeError(f'{path} is not a PageXML file!')

    return bs


def page_xml_to_bs4(path: str) -> BeautifulSoup:
    """Generates BeautifulSoup Object from file path

    Args:
        path: file path string

    Returns:
        BeautifulSoup: BeautifulSoup4 object
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return BeautifulSoup(data, 'xml')


def extract_data(bs: BeautifulSoup, xml_id: str) -> PageXML:
    """ Extracts data from valid PageXML file (BeautifulSoup object)

    Args:
        xml_id: name of xml file
        bs: BeautifulSoup object of PageXML file

    Returns:
        Extracted data (PageXML object)
    """
    xml = PageXML(id=xml_id)
    for page in bs.find_all('Page'):
        p: Page = Page(
            file=page.attrs.get('imageFilename'),
            height=int(page.attrs.get('imageHeight')),
            width=int(page.attrs.get('imageWidth'))
        )
        for region in page.find_all('TextRegion'):
            # text region -> irrelevant information
            for line in region.find_all('TextLine'):
                p.lines.append(Line(
                    id=line.attrs.get('id'),
                    text=line.find('Unicode').text,
                    coords=numpy.array([[int(x) for x in y.split(',')] for y in line.find('Coords').attrs.get('points').split(' ')], dtype=numpy.int32)
                ))
        xml.pages.append(p)
    return xml
