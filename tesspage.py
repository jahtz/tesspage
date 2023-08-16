from argparse import ArgumentParser, Namespace
import pathlib
import os

from pagexml.parser import parse_page_xml
from ground_truth.converter import xml_to_line_gt


def cli():
    parser = ArgumentParser(
        description='Toolset for Tesseract training with PageXML Ground-Truth',
        epilog='GitHub: https://github.com/Jatzelberger/tesspage'
    )

    parser.add_argument('-s', '--setup', action='store_true',
                        help="Creates necessary file structure and downloads repositories")
    parser.add_argument('-g', '--generate', action='store_true',
                        help="Generates ground truth data from PageXML, requires INPUT_DIR, OUTPUT_DIR")
    parser.add_argument('-t', '--train', action='store_true',
                        help='starts training process, requires INPUT_DIR"')

    parser.add_argument('INPUT_DIR', nargs='?', default=None,
                        help='Folder containing PageXML files and matching images')
    parser.add_argument('OUTPUT_DIR', nargs='?', default=None,
                        help='Folder containing processed Ground-Truth')

    args = parser.parse_args()

    if args.setup:
        setup()
    if args.generate:
        if args.INPUT_DIR is not None and args.OUTPUT_DIR is not None:
            generate(args)
        else:
            parser.print_help()
    if args.train:
        if args.INPUT_DIR is not None:
            train()
        else:
            parser.print_help()


def setup():
    if input('tesseract-ocr, libtesseract-ocr, libtool, pkg-config, make, wget, find, bash, unzip, bc and git installed? [Y/n]').lower() in ['y', 'yes']:
        if not pathlib.Path('./tesstrain').exists():
            os.system('git clone https://github.com/tesseract-ocr/tesstrain')  # fetch tesstrain repository
        if not pathlib.Path('./tessdata_best').exists():
            os.system('git clone https://github.com/tesseract-ocr/tessdata_best')  # fetch tessdata_best repository

        os.mkdir('./input')  # create default folders
        os.mkdir('./output')

        os.chdir('./tesstrain')
        os.system('make tesseract-langdata')  # fetch tesseract config and create data dir


def generate(args: Namespace):
    if not pathlib.Path(args.INPUT_DIR).exists():
        raise Exception('Input directory does not exist!')  # check, if input folder exists
    xml_files = [file for file in pathlib.Path(args.INPUT_DIR).glob('*.xml')]  # get list of all xml files in input_dir
    xml_files.sort()
    for file in xml_files:
        print(f'{file.name}:')
        xml = parse_page_xml(file.as_posix())  # parse files
        print(f'\t{xml_to_line_gt(xml, args.OUTPUT_DIR)}')  # generate ground truth files
    print('Done!')

def train():
    pass


if __name__ == '__main__':
    cli()
