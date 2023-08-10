import sys
from enum import Enum

Mode = Enum('Mode', [('PREPARE', 0), ('PREPARE_AND_TRAIN', 1), ('TRAIN', 2), ('PURGE', 3)])


class TessPage:
    def __init__(self):
        self.input_dir: str
        self.output_dir: str
        self.mode: Mode

    def run(self, args: list):
        self.mode = self.read_cli(args)

    def read_cli(self, args: list) -> Mode:
        if len(args) > 0:
            match (args[0]):
                case '-p':
                    pass
                case '-pt':
                    pass
                case '-t':
                    pass
                case '-c':
                    pass
                case _:
                    # default: help
                    print_help()
        else:
            # help
            print_help()


def print_help():
    print("""
    -p <input_dir> <output_dir>: prepare data
    -pt <input_dir> <output_dir>: prepare data and train
    -t <input_dir>: train
    -c <dir>: purge prepared data
    """)


if __name__ == '__main__':
    TessPage().run(sys.argv[1:])
