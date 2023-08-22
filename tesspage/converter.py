import os
import cv2
import numpy
from pathlib import Path

from tesspage.document import Document


def xml_to_line_gt(xml: Document, output_dir: Path) -> str:
    """
    Crops image to line ground truth data based on PageXML data

    :param xml: PageXMLReader object
    :param output_dir: where ground truth data will be stored
    :return: status string
    """

    if not output_dir.exists():
        os.mkdir(output_dir.as_posix())

    page_counter: int = 0
    region_counter: int = 0
    line_counter: int = 0

    for page in xml.pages:
        img = cv2.imread(page.file)
        mask = numpy.zeros((page.height, page.width), dtype=numpy.uint8)
        for region in page.text_regions:
            for line in region.text_lines:
                cv2.fillPoly(mask, numpy.int32([numpy.array(line.coords, dtype=numpy.int32)]), (255, 255, 255))
                res = cv2.bitwise_and(img, img, mask=mask)
                rect = cv2.boundingRect(numpy.array(line.coords, dtype=numpy.int32))
                bg = numpy.full((res.shape[0], res.shape[1], 3), (255, 255, 255), dtype=numpy.uint8)
                mask_inverted = cv2.bitwise_not(mask)
                bg_cropped = cv2.bitwise_or(bg, bg, mask=mask_inverted)
                final_img = res + bg_cropped
                cropped = final_img[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

                filename = f'{xml.id}-{page.id}-{region.id}-{line.id}'
                cv2.imwrite(output_dir.joinpath(filename + '.png').as_posix(), cropped)
                with open(output_dir.joinpath(filename + '.gt.txt').as_posix(), 'w', encoding='utf-8') as f:
                    f.write(line.text)

                line_counter += 1
            region_counter += 1
        page_counter += 1
    return f'Cropped {line_counter} line(s) from {region_counter} region(s) on {page_counter} page(s)'
