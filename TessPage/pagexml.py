import pathlib
import numpy
from bs4 import BeautifulSoup


class PageXML:
    def __init__(self, pagexml_path: str) -> None:
        self.fp = pagexml_path  # file pointer
        self.bs: BeautifulSoup = self.__check_for_valid_file()
          
    def __str__(self) -> str:
        return f'PageXML Object ({self.fp})'
    
    def __check_for_valid_file(self) -> BeautifulSoup:
        if (not pathlib.Path(self.fp).exists()):
            raise FileNotFoundError(f'{self.fp} does not exist!')
        if (not pathlib.Path(self.fp).is_file()):
            raise IsADirectoryError(f'{self.fp} is a directory!')
        if (not pathlib.Path(self.fp).suffix != 'xml'):
            raise TypeError(f'{self.fp} is no .xml file!')
        
        bs = self.__unpack_xml()
        xml_data = bs.find('PcGts')
        if not ((xml_data)
                and ('xmlns' in xml_data.attrs) 
                and ('http://schema.primaresearch.org/PAGE/gts/pagecontent/' in xml_data.attrs.get('xmlns'))
                ):  # check if file uses page scheme
            raise TypeError(f'{self.fp} is not a PageXML file!')
        
        return bs
        
    def __unpack_xml(self) -> BeautifulSoup:
        """Generates BeautifulSoup Object from file path

        Returns:
            BeautifulSoup: BS4 Object
        """
        with open(self.fp, 'r', encoding='utf-8') as f:
            data = f.read()
        return BeautifulSoup(data, 'xml')
    
    def get_data(self) -> dict:
        """Extracts data from PageXML file

        Returns:
            dict: Extracted Data in format:
            
            [
                {
                    pagePath: str,
                    pageHeight: int,
                    pageWidth: int,
                    lines: [
                        {
                            lineId: str,
                            lineCoords: numpyArray,
                            lineText: str,
                        }
                    ]
                }
            ]
        """
        data = []
        for page in self.bs.find_all('Page'):
            page_data = {
                'pagePath': page.attrs.get('imageFilename'),
                'pageHeight': page.attrs.get('imageHeight'),
                'pageWidth': page.attrs.get('imageWidth'),
                'lines': [],
            }
            for region in page.find_all('TextRegion'):
                # textregions irrelevant
                for line in region.find_all('TextLine'):
                    line_data = {
                        'lineId': line.attrs.get('id'),
                        'lineCoords': numpy.array([[int(x) for x in y.split(',')] for y in line.find('Coords').attrs.get('points').split(' ')], dtype=numpy.int32),
                        'lineText': line.find('Unicode').text,
                    }
                    page_data['lines'].append(line_data)
            data.append(page_data)
        return data
        
if __name__ == '__main__':
    a = PageXML('Examples/0001.xml')
    print(a.get_data())