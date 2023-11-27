from pathlib import Path

from lxml import etree

from tesspage.document import Document


class PageXMLBuilder:
    def __init__(self, document: Document):
        self.doc = document

    def build(self, target_file: Path) -> None:
        """
        Writes Document object to file

        Args:
            target_file: filepath + name + .xml
        """
        root = etree.Element('PcGts', xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15")
        metadata = etree.Element('Metadata')
        if self.doc.creator != '':
            creator = etree.Element('Creator')
            creator.text = self.doc.creator
            metadata.append(creator)
        if self.doc.created != '':
            created = etree.Element('Created')
            created.text = self.doc.created
            metadata.append(created)
        if self.doc.last_change != '':
            last_change = etree.Element('LastChange')
            last_change.text = self.doc.last_change
            metadata.append(last_change)

        root.append(metadata)

        for p in self.doc.pages:
            page = etree.Element('Page', imageFilename=Path(p.file).name, imageHeight=str(p.height), imageWidth=str(p.width))
            for r in p.text_regions:
                region = etree.Element('TextRegion', id=r.id)
                region.append(etree.Element('Coords', points=self.__coords_formatter(r.coords)))
                for l in r.text_lines:
                    line = etree.Element('TextLine', id=l.id)
                    line.append(etree.Element('Coords', points=self.__coords_formatter(l.coords)))
                    # unicode tag
                    unicode = etree.Element('Unicode')
                    unicode.text = l.text

                    # textequiv tag
                    textequiv = etree.Element('TextEquiv', index='0')
                    textequiv.append(unicode)

                    line.append(textequiv)
                    region.append(line)
                page.append(region)
            root.append(page)

        with open(target_file.as_posix(), 'w') as f:
            f.write(etree.tostring(root, pretty_print=True).decode('UTF-8'))

    def __coords_formatter(self, coords: list) -> str:
        """
        Format coords list to matching string

        Args:
            coords: nested coords list [[x0, y0],...]

        Returns:
            coords string
        """
        c = []
        for xy in coords:
            c.append(f'{xy[0]},{xy[1]}')
        return ' '.join(c)


def build_xml_file(data: Document, target_file: Path) -> None:
    """
    Writes xml file from Document object

    Args:
        data: Document object
        target_file: target path + filename + .xml
    """
    PageXMLBuilder(data).build(target_file)
