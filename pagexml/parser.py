import pathlib
from bs4 import BeautifulSoup

from pagexml.objects import Page, TextRegion, TextLine


class PageXMLReader:
    def __init__(self, path: str):
        self.id: str = ''
        self.path: str = pathlib.Path(path).absolute().as_posix()
        self.creator: str = ''
        self.created: str = ''
        self.last_change: str = ''
        self.pages: list[Page] = []
        self.__parse(self.__check_valid())

    def __check_valid(self) -> BeautifulSoup:
        """
        Check for valid PageXML formatting

        :return: BeautifulSoup object of xml file
        """
        if not pathlib.Path(self.path).exists():
            raise FileNotFoundError(self.path + 'does not exist!')
        if not pathlib.Path(self.path).is_file():
            raise IsADirectoryError(self.path + 'is a directory!')
        if not pathlib.Path(self.path).suffix != 'xml':
            raise TypeError(self.path + 'is no .xml file!')

        with open(self.path, 'r', encoding='utf-8') as f:
            data = f.read()
        bs = BeautifulSoup(data, 'xml')

        xml_data = bs.find('PcGts')
        if not (xml_data
                and ('xmlns' in xml_data.attrs)
                and ('http://schema.primaresearch.org/PAGE/gts/pagecontent/' in xml_data.attrs.get('xmlns'))
                ):  # check if file uses page scheme
            raise TypeError(self.path + 'is not a PageXML file!')
        return bs

    def __parse(self, bs: BeautifulSoup) -> None:
        """
        Starts parsing of file

        :param bs: BeautifulSoup object of xml file
        :return: None
        """
        self.id = pathlib.Path(self.path).name.replace('.xml', '')
        self.__parse_meta(bs.find('Metadata'))
        self.__parse_page(bs)

    def __parse_meta(self, meta) -> None:
        """
        Parses meta data

        :param meta: BeautifulSoup object of meta data
        :return: None
        """
        creator = meta.find('Creator')
        if creator is not None:
            self.creator = creator.text

        created = meta.find('Created')
        if created is not None:
            self.created = created.text

        last_change = meta.find('LastChange')
        if last_change is not None:
            self.last_change = last_change.text

    def __parse_page(self, bs) -> None:
        """
        Parses page data

        :param bs: BeautifulSoup object of xml file
        :return: None
        """
        page_counter = 0
        for page in bs.find_all('Page'):
            p = Page(
                id=f'p_{page_counter}',
                file=pathlib.Path(self.path).parent.joinpath(page.attrs.get('imageFilename')).as_posix(),
                height=int(page.attrs.get('imageHeight')),
                width=int(page.attrs.get('imageWidth'))
            )
            for region in page.find_all('TextRegion'):
                r = TextRegion(
                    id=region.attrs.get('id'),
                    custom=region.attrs.get('custom'),
                    coords=[[int(x) for x in y.split(',')] for y in
                            region.find('Coords').attrs.get('points').split(' ')]
                )
                for line in region.find_all('TextLine'):
                    l = TextLine(
                        id=line.attrs.get('id'),
                        text=line.find('Unicode').text,
                        coords=[[int(x) for x in tuples.split(',')] for tuples in
                                line.find('Coords').attrs.get('points').split(' ')],
                    )
                    r.text_lines.append(l)
                p.text_regions.append(r)
            self.pages.append(p)
            page_counter += 1


def parse_page_xml(path: str) -> PageXMLReader:
    """ Returns immutable PageXML object

    :param path: absolute path to PageXML file
    :return: PageXML object
    """
    return PageXMLReader(path)
