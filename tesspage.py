import pathlib
import os

from docopt import docopt

from tesspage.pagexml_parser import parse_page_xml
from tesspage.converter import xml_to_line_gt

cli_doc = """TessPage Command Line Tool
Toolset for Tesseract training with PageXML Ground-Truth

Usage:
    tesspage.py (-h | --help)
    tesspage.py (-v | --version)
    tesspage.py setup
    tesspage.py generate [--training_data <folder>] [--ground_truth <folder>]
    tesspage.py training [--model_name <name>] [--start_model <model>] [--data_dir <folder>] [--ground_truth <folder>] [--tessdata <folder>] [--max_iterations <number>] [ARGS ...]
    tesspage.py tesseract --model_name <name> [--input <path>] [--output <path>] [--data_dir <folder>] [--config_dir <config_dir>] [--config <config>] [ARGS ...]
    tesspage.py eval ARGS

Options:
    -h --help                       Show this screen.
    -v --version                    Show version.
    setup                           Download and setup tesspage, tesstrain and tesseract.
    generate                        Generate Ground-Truth from PageXML files.
    training                        Train Model.
    tesseract                       Run Tesseract.
    eval                            Evaluate quality of model. (Not implemented)
    --training_data <folder>        Input PageXML folder for training. [default: ./data/training_data/]
    --ground_truth <folder>         Ground Truth folder. [default: ./data/ground_truth/]
    --model_name <name>             Name of the model to be built. [default: foo]
    --start_model <model>           Name of the model to continue from. [default: eng]
    --data_dir <folder>             Data directory for output files, proto model, start model, etc. [default: ./tesstrain/data/]
    --tessdata <folder>             Path to the .traineddata directory to start finetuning from. [default: ./data/tessdata_best/]
    --max_iterations <number>       Max iterations. [default: 10000]
    --input <path>                  Input file/directory. [default: ./data/ocr_input/]
    --output <path>                 Output Directory [default: ./data/ocr_output/]
    --config_dir <config_dir>       Output config directory. [default: ./data/tessconfigs/configs/]
    --config <config>               Output config. [default: txt]
    ARGS                            Additional arguments
"""


def cli():
    args = docopt(cli_doc, help=True, version='tesspage v1.0', options_first=False)
    print(args)

    if args.get('setup'):
        setup()

    elif args.get('generate'):
        generate_ground_truth(
            page_input_dir=args.get('--training_data'),
            gt_output_dir=args.get('--ground_truth')
        )

    elif args.get('training'):
        train(
            model_name=args.get('--model_name'),
            start_model=args.get('--start_model'),
            data_dir=pathlib.Path(args.get('--data_dir')).absolute().as_posix(),
            ground_truth_dir=pathlib.Path(args.get('--ground_truth')).absolute().as_posix(),
            tessdata=pathlib.Path(args.get('--tessdata')).absolute().as_posix(),
            max_iterations=args.get('--max_iterations'),
            args=" ".join(args.get('ARGS'))
        )

    elif args.get('tesseract'):
        tesseract(
            model_name=args.get('--model_name'),
            input_dir=pathlib.Path(args.get('--input')).absolute().as_posix(),
            output_dir=pathlib.Path(args.get('--output')).absolute().as_posix(),
            data_dir=pathlib.Path(args.get('--data_dir')).absolute().as_posix(),
            config_dir=pathlib.Path(args.get('--config_dir')).absolute().as_posix(),
            config=args.get('--config'),
            args=" ".join(args.get('ARGS'))
        )

    elif args.get('eval'):
        print('Coming soon')

    else:
        print('Something went wrong!')


def setup() -> None:
    if input('tesseract-ocr, libtesseract-ocr, libtool, pkg-config, make, wget, find, bash, unzip, bc and git '
             'installed? [Y/n]: ').lower() in ['y', 'yes']:

        if not pathlib.Path('./tesstrain').exists():
            os.system('git clone https://github.com/tesseract-ocr/tesstrain')  # fetch tesstrain repository

        if not pathlib.Path('./data').exists():
            os.mkdir('data')  # create folder for tesseract data

        os.chdir('./data')

        if not pathlib.Path('./training_data').exists():
            os.mkdir('./training_data')  # create default folder for pagexml input

        if not pathlib.Path('./ground_truth').exists():
            os.mkdir('./ground_truth')  # create default ground_truth folder

        if not pathlib.Path('./ocr_input').exists():
            os.mkdir('./ocr_input')  # create default folder for ocr input

        if not pathlib.Path('./ocr_output').exists():
            os.mkdir('./ocr_output')  # create default folder for ocr output

        if not pathlib.Path('./eval').exists():
            os.mkdir('./eval')  # create default folder for model evaluation

        if not pathlib.Path('./tessconfigs').exists():
            os.system('git clone https://github.com/tesseract-ocr/tessconfigs.git')  # fetch tesseract config data

        if not pathlib.Path('./tessdata_best').exists():
            os.system('git clone https://github.com/tesseract-ocr/tessdata_best')  # fetch tessdata_best repository

        os.chdir('../tesstrain')
        os.system('make tesseract-langdata')  # fetch tesseract config and create data dir

        print('Done!')

    else:
        print('run: sudo apt install -y tesseract-ocr libtesseract-dev libtool pkg-config make wget bash unzip bc')


def generate_ground_truth(page_input_dir: str, gt_output_dir: str) -> None:
    if not pathlib.Path(page_input_dir).exists():
        raise Exception('Input directory does not exist!')  # check, if input folder exists
    xml_files = [file for file in pathlib.Path(page_input_dir).glob('*.xml')]  # get list of all xml files in input_dir
    xml_files.sort()
    for file in xml_files:
        print(f'{file.name}:')
        xml = parse_page_xml(file.as_posix())  # parse files
        print(f'\t{xml_to_line_gt(xml, gt_output_dir)}')  # generate ground truth files
    print('Done!')


def train(model_name: str, start_model: str, data_dir: str, ground_truth_dir: str, tessdata: str, max_iterations: str,
          args: str) -> None:
    os.chdir('./tesstrain')
    cmd = f'make training MODEL_NAME={model_name} START_MODEL={start_model} DATA_DIR={data_dir} GROUND_TRUTH_DIR={ground_truth_dir} TESSDATA={tessdata} MAX_ITERATIONS={max_iterations} {args}'
    os.system(cmd)


def tesseract(model_name: str, input_dir: str, output_dir: str, data_dir: str, config_dir: str,
              config: str, args: str) -> None:
    cfg = os.path.join(config_dir, config)
    if pathlib.Path(input_dir).is_file():
        output = os.path.join(output_dir, os.path.splitext(pathlib.Path(input_dir).name)[0])
        cmd = f'tesseract {input_dir} {output} --tessdata-dir {data_dir} -l {model_name} {cfg} {args}'
        os.system(cmd)
    elif pathlib.Path(input_dir).is_dir():
        images = [file for file in pathlib.Path(input_dir).glob('*.*')]  # get list of all xml files in input_dir
        images.sort()
        if config.lower() == 'pagexml':
            pass  # TODO: implement pagexml parser
        else:
            for image in images:
                print(f'{image}:')
                output = os.path.join(output_dir, os.path.splitext(pathlib.Path(image).name)[0])
                cmd = f'tesseract {image} {output} --tessdata-dir {data_dir} -l {model_name} {cfg} {args}'
                os.system(cmd)
        print('Done!')
    else:
        print('Input not found')


if __name__ == '__main__':
    cli()
