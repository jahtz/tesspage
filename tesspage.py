import os
from pathlib import Path
from docopt import docopt

from tesspage.pagexml_parser import parse_pagexml
from tesspage.pagexml_builder import build_xml_file
from tesspage.hocr_parser import parse_hocr
from tesspage.converter import xml_to_line_gt
from tesspage.helper import abs_path, file_list, file_to_string
from tesspage.eval import evaluate_cer, evaluate_wer


cli_doc = """TessPage Command Line Tool
Toolset for Tesseract training with PageXML Ground-Truth

Usage:
    tesspage.py (-h | --help)
    tesspage.py (-v | --version)
    tesspage.py setup
    tesspage.py generate [--training_data <folder>] [--ground_truth <folder>]
    tesspage.py training [--model_name <name>] [--start_model <model>] [--data_dir <folder>] [--ground_truth <folder>] [--tessdata <folder>] [--max_iterations <number>] [ARGS ...]
    tesspage.py tesseract --model_name <name> [--input <path>] [--output <path>] [--data_dir <folder>] [--config_dir <config_dir>] [--config <config>] [ARGS ...]
    tesspage.py eval [--eval_input <folder>]

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
    --eval_input <folder>           Folder containing evaluation files [default: ./data/eval/]
    --reference <file>              Supports .txt, .hocr .xml (pagexml) files [default: ./data/eval/reference.txt]
    --prediction <file>             Supports .txt, .hocr .xml (pagexml) files [default: ./data/eval/prediction.txt]
    ARGS                            Additional arguments
    
Guide:
    https://github.com/Jatzelberger/tesspage
"""


def cli() -> None:
    """ Parsing CLI input """
    args = docopt(cli_doc, help=True, version='tesspage v1.0', options_first=False)

    if args.get('setup'):
        setup()

    elif args.get('generate'):
        generate_ground_truth(
            page_input_dir=abs_path(args.get('--training_data')),
            gt_output_dir=abs_path(args.get('--ground_truth')),
        )

    elif args.get('training'):
        training(
            model_name=args.get('--model_name'),
            start_model=args.get('--start_model'),
            data_dir=abs_path(args.get('--data_dir')),
            ground_truth_dir=abs_path(args.get('--ground_truth')),
            tessdata=abs_path(args.get('--tessdata')),
            max_iterations=args.get('--max_iterations'),
            args=" ".join(args.get('ARGS'))
        )

    elif args.get('tesseract'):
        tesseract(
            model_name=args.get('--model_name'),
            input_dir=abs_path(args.get('--input')),
            output_dir=abs_path(args.get('--output')),
            data_dir=abs_path(args.get('--data_dir')),
            config_dir=abs_path(args.get('--config_dir')),
            config=args.get('--config'),
            args=" ".join(args.get('ARGS'))
        )

    elif args.get('eval'):
        evaluate(
            eval_folder=abs_path(args.get('--eval_input'))
        )

    else:
        print('Something went wrong!')


def setup() -> None:
    """ Creates and downloads necessary files and folders"""
    if input('tesseract-ocr, libtesseract-ocr, libtool, pkg-config, make, wget, find, bash, unzip, bc and git '
             'installed? [Y/n]: ').lower() in ['y', 'yes']:

        if not Path('./tesstrain').exists():
            os.system('git clone https://github.com/tesseract-ocr/tesstrain')  # fetch tesstrain repository

        if not Path('./data').exists():
            os.mkdir('data')  # create folder for tesseract data

        os.chdir('./data')

        if not Path('./training_data').exists():
            os.mkdir('./training_data')  # create default folder for pagexml input

        if not Path('./ground_truth').exists():
            os.mkdir('./ground_truth')  # create default ground_truth folder

        if not Path('./ocr_input').exists():
            os.mkdir('./ocr_input')  # create default folder for ocr input

        if not Path('./ocr_output').exists():
            os.mkdir('./ocr_output')  # create default folder for ocr output

        if not Path('./eval').exists():
            os.mkdir('./eval')  # create default folder for model evaluation

        if not Path('./tessconfigs').exists():
            os.system('git clone https://github.com/tesseract-ocr/tessconfigs.git')  # fetch tesseract config data

        if not Path('./tessdata_best').exists():
            os.system('git clone https://github.com/tesseract-ocr/tessdata_best')  # fetch tessdata_best repository

        os.chdir('../tesstrain')
        os.system('make tesseract-langdata')  # fetch tesseract config and create data dir

        print('Done!')

    else:
        print('run: sudo apt install -y tesseract-ocr libtesseract-dev libtool pkg-config make wget bash unzip bc')


def generate_ground_truth(page_input_dir: Path, gt_output_dir: Path) -> None:
    """
    Logic for parsing a set of image + pagexml files to line-image + text files

    Args:
        page_input_dir: folder containing image + pagexml pairs
        gt_output_dir: output folder
    """
    if not page_input_dir.exists():
        raise Exception('Input directory does not exist!')

    for file in file_list(page_input_dir, 'xml'):
        print(f'{file.name}:')
        xml = parse_pagexml(file)  # parse files to document object
        print(f'\t{xml_to_line_gt(xml, gt_output_dir)}')  # generate line image and text files from document object
    print('Done!')


def training(model_name: str, start_model: str, data_dir: Path, ground_truth_dir: Path, tessdata: Path, max_iterations: str, args: str) -> None:
    """
    Start Tesseract training

    Args:
        model_name: Name of the model to be built
        start_model: Name of the model to continue from
        data_dir: Data directory for output files, proto model, start model, etc.
        ground_truth_dir: Ground Truth folder
        tessdata: Path to the .traineddata directory to start finetuning from
        max_iterations: training iterations
        args: custom args for training
    """
    os.chdir('./tesstrain')
    cmd = f'make training MODEL_NAME={model_name} START_MODEL={start_model} DATA_DIR={data_dir} GROUND_TRUTH_DIR={ground_truth_dir} TESSDATA={tessdata} MAX_ITERATIONS={max_iterations} {args}'
    os.system(cmd)


def tesseract(model_name: str, input_dir: Path, output_dir: Path, data_dir: Path, config_dir: Path, config: str, args: str) -> None:
    """
    Start Tesseract OCR
    Args:
        model_name: Name of model to be used
        input_dir: folder containing images
        output_dir: folder for file output
        data_dir: Data directory for output files, proto model, start model, etc.
        config_dir: Output config directory
        config: output format
        args: custom args for ocr
    """
    cfg = config_dir.joinpath(config)  # config path

    # single file
    if input_dir.is_file():

        # custom pagexml config
        if config.lower() == 'pagexml':
            temp_folder = output_dir.joinpath('temp')  # create temp folder
            if not temp_folder.exists():
                os.mkdir(temp_folder.as_posix())
            page_tesseract(input_dir, output_dir, temp_folder, data_dir, model_name, config_dir, args)  # run tesseract on file

        # default configs
        else:
            output = output_dir.joinpath(os.path.splitext(input_dir.name)[0])  # output base: output_dir + filename
            run_tesseract(input_dir, output, data_dir, model_name, cfg, args)  # run tesseract
        print('Done!')

    # directory
    elif input_dir.is_dir():
        images = file_list(input_dir, '*')
        if config.lower() == 'pagexml':
            temp_folder = output_dir.joinpath('temp')  # create temp folder
            if not temp_folder.exists():
                os.mkdir(temp_folder.as_posix())

            for image in images:
                print(f'{image}:')
                page_tesseract(image, output_dir, temp_folder, data_dir, model_name, config_dir, args)  # run tesseract on every file

        else:
            for image in images:
                print(f'{image}:')
                output = output_dir.joinpath(os.path.splitext(image.name)[0])  # output base: output_dir + filename
                run_tesseract(image, output, data_dir, model_name, cfg, args)  # run tesseract
        print('Done!')

    else:
        print('Input not found')


def run_tesseract(input_dir: Path, output_base: Path, data_dir: Path, model_name: str, cfg: Path, args: str) -> None:
    """
    Run Tesseract CLI with given arguments

    Args:
        input_dir: folder containing images
        output_base: output_dir + filename without extension
        data_dir: Data directory for output files, proto model, start model, etc.
        model_name: Name of model to be used
        cfg: config_dir + config
        args: custom args for ocr
    """
    cmd = f'tesseract {input_dir} {output_base} --tessdata-dir {data_dir} -l {model_name} {cfg} {args}'
    os.system(cmd)  # create file <output_base>.<config>


def page_tesseract(input_dir: Path, output_dir: Path, temp_folder: Path, data_dir: Path, model_name: str, config_dir: Path, args: str) -> None:
    """
    Run Tesseract and parse to pagexml

    Args:
        input_dir: folder containing images
        output_dir: folder for file output
        temp_folder: folder for temp hocr files
        data_dir: Data directory for output files, proto model, start model, etc.
        model_name: Name of model to be used
        config_dir: Output config directory
        args: custom args for ocr
    """
    temp_base = temp_folder.joinpath(os.path.splitext(input_dir.name)[0])  # temp base in temp folder
    hocr_cfg = config_dir.joinpath('hocr')  # set tesseract config to hocr
    run_tesseract(input_dir, temp_base, data_dir, model_name, hocr_cfg, args)  # run tesseract on file

    hocr_file = parse_hocr(Path(temp_base.as_posix() + '.hocr'))  # read hocr file in temp folder
    output = output_dir.joinpath(os.path.splitext(input_dir.name)[0] + '.xml')  # create base for main output folder
    build_xml_file(data=hocr_file, target_file=output)  # write pagexml file to main output folder

    os.system(f'rm {temp_base}.hocr')  # remove temp file


def evaluate(eval_folder: Path) -> None:
    """
    Evaluate model precision, prints result

    Args:
        eval_folder: folder containing eval files, pred with .extension, gt with .gt.extension. Supports .txt, .hocr and .xml (page)
    """
    cer_list = []
    wer_list = []

    ref_files: list[Path] = file_list(eval_folder, 'gt.*')
    for ref_path in ref_files:
        try:
            pred_path = ref_path.parent.joinpath('.'.join(ref_path.name.split('.')[0:-2]) + ref_path.suffix)
            ref = file_to_string(ref_path)
            pred = file_to_string(pred_path)
            cer = float(evaluate_cer(ref, pred))
            cer_list.append(cer)
            wer = float(evaluate_wer(ref, pred))
            wer_list.append(wer)
            print('{0}/{1}: CER {2:.4f}%, WER: {3:.4}%'.format(ref_path.name, pred_path.name, cer * 100, wer * 100))
        except Exception:
            print(f'{ref_path.name}/No matching file found')
    if len(cer_list) == 0 or len(wer_list) == 0:
        print('Summary:\nNo values!')
    else:
        print('\nSummary:\nCER {0:.4f}%\nWER {1:.4f}%'.format((sum(cer_list) / len(cer_list)) * 100, (sum(wer_list) / len(wer_list)) * 100))


if __name__ == '__main__':
    cli()
