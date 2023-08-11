from PageXMLParser.structure import PageXML
import PageXMLParser.page_xml_parser
import numpy
import cv2
import os
import pathlib


def generate_line_images(xml_data: PageXML, input_dir: str, output_dir: str) -> str:
    """ Generates valid data for TessTrain from xml data

    Args:
        xml_data: previously generated xml data in
        input_dir: directory, where xml and png are saved
        output_dir: directory, where images and ground truth text should be stored

    Returns:
        Work summary
    """
    input_dir = pathlib.Path(input_dir).absolute()
    output_dir = pathlib.Path(output_dir).absolute()

    if not pathlib.Path(input_dir.as_posix()).exists() or not pathlib.Path(input_dir.as_posix()).is_dir():
        return 'Input directory does not exist'
    if not pathlib.Path(output_dir.as_posix()).exists():
        os.mkdir(output_dir.as_posix())

    page_counter: int = 0
    line_counter: int = 0
    for page in xml_data.pages:
        img = cv2.imread(pathlib.Path(input_dir).absolute().joinpath(page.file).as_posix())
        mask = numpy.zeros((page.height, page.width), dtype=numpy.uint8)
        for line in page.lines:
            cv2.fillPoly(mask, numpy.int32([line.coords]), (255, 255, 255))
            res = cv2.bitwise_and(img, img, mask=mask)
            rect = cv2.boundingRect(line.coords)

            bg = numpy.full((res.shape[0], res.shape[1], 3), (255, 255, 255), dtype=numpy.uint8)
            mask_inverted = cv2.bitwise_not(mask)
            bg_cropped = cv2.bitwise_or(bg, bg, mask=mask_inverted)

            final_img = res + bg_cropped
            cropped = final_img[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

            filename = name_generator(xml_data.id, str(page_counter), str(line_counter))
            # show_image(filename, cropped)
            cv2.imwrite(output_dir.joinpath(filename + '.png').as_posix(), cropped)
            with open(output_dir.joinpath(filename + '.gt.txt').as_posix(), 'w', encoding='utf-8') as f:
                f.write(line.text)
            line_counter += 1
        page_counter += 1

    return f'{xml_data.id}.xml: Cropped {line_counter} line(s) from {page_counter} page(s)'


def show_image(name: str, img) -> None:
    """Opens cropped image preview

    Args:
        name: window name
        img: image data

    Returns:
        None
    """
    cv2.imshow(name, img)
    cv2.waitKey(0)  # wait for close


def name_generator(xml_id: str, page_id: str, line_id: str) -> str:
    """ Generates valid name

    Args:
        xml_id: xml file name
        page_id: page id
        line_id: line id

    Returns:
        valid string
    """
    return f'{xml_id}-p{page_id}-l{line_id}'
