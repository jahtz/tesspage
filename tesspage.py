from argparse import ArgumentParser
import pathlib
import os
from PageXMLParser.page_xml_parser import check_valid_page_xml, extract_data
from PageXMLParser.image_cropper import generate_line_images


def init_cli():
    parser = ArgumentParser(
        description='Convert full page image files and convert to single line images and ground truth text files for tesseract training',
        epilog='GitHub: https://github.com/Jatzelberger/TessPage'
    )
    parser.add_argument('-c', '--convert', action='store_true',
                        help="Convert files")
    parser.add_argument('-f', '--full', action='store_true',
                        help="Convert files and train tesseract (not implemented)")
    parser.add_argument('-t', '--train', action='store_true',
                        help="Train tesseract with data from output_dir (not implemented)")
    parser.add_argument('-p', '--purge', action='store_true',
                        help="Purge output dir (not implemented)")
    parser.add_argument('input_dir', nargs='?',
                        help='Directory with full page image and matching PageXML files')
    parser.add_argument('output_dir',
                        help='Directory for output of converted data')

    args = parser.parse_args()
    if args.convert and (args.input_dir is not None):
        handle_convert(args)
    else:
        print(args)
        parser.print_help()


def handle_convert(args):
    if not pathlib.Path(args.input_dir).exists():
        # check, if input folder exists
        raise Exception('Input directory does not exist!')

    # create list of .xml files in input folder
    xml_files = [xml for xml in os.listdir(args.input_dir) if xml.endswith('.xml')]

    if len(xml_files) < 1:
        # check if .xml files exist
        raise Exception('Input directory does not contain any .xml files')

    if not pathlib.Path(args.output_dir).exists():
        # create output directory if non-existent
        os.mkdir(args.output_dir)

    # convert files
    for xml in xml_files:
        xml_id = xml.replace('.xml', '')
        bs = check_valid_page_xml(args.input_dir + '\\' + xml)
        print(generate_line_images(extract_data(bs, xml_id), args.input_dir, args.output_dir))
    print('Done!')


if __name__ == '__main__':
    init_cli()
