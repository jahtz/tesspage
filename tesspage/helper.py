from pathlib import Path
from .hocr_parser import hocr_to_string
from .pagexml_parser import pagexml_to_string


def abs_path(rel_path: str) -> Path:
    """
    Builds absolute path from relative path
    Args:
        rel_path: relative path

    Returns:
        absolute path
    """
    return Path(rel_path).absolute()


def file_list(dir_path: Path, extension: str) -> list:
    """
    Creates a list of files within a folder
    Args:
        extension: file extension without '.'
        dir_path: folder path

    Returns:
        Sorted list of files within given folder, empty list on bad path
    """
    if dir_path.is_dir():
        files = [file for file in dir_path.glob(f'*.{extension}')]  # get list of all xml files in input_dir
        files.sort()
        return files
    else:
        return []


def file_to_string(file: Path) -> str:
    suffix = file.suffix
    if suffix == '.txt':
        with open(file, 'r') as f:
            text = f.read()
        return text
    elif suffix == '.hocr':
        return hocr_to_string(file)
    elif suffix == '.xml':
        return pagexml_to_string(file)
    else:
        msg = f'{file}: unsupported format'
        raise TypeError(msg)
