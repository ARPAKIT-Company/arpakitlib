# arpakit

import sys

from arpakitlib.ar_parse_command import parse_command


def _cli():
    parsed_command = parse_command(text=" ".join(sys.argv))
    parsed_command.raise_for_command(needed_command="arpakitlib", lower_=True)

    print(parsed_command)


def __example():
    _cli()


if __name__ == '__main__':
    __example()
