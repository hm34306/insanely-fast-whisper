import argparse
import json
import os
from typing import TypeVar

T = TypeVar('T', bound='TxtFormatter')

class TxtFormatter:
    @classmethod
    def preamble(cls:type[T]) -> str:
        return ""

    @classmethod
    def format_chunk(cls:type[T], chunk: str, index: int) -> str:
        text = chunk['text']
        return f"{text}\n"

T = TypeVar('T', bound='SrtFormatter')

class SrtFormatter:
    @classmethod
    def preamble(cls:type[T]) -> str:
        return ""

    @classmethod
    def format_seconds(cls:type[T], seconds: int) -> str:
        whole_seconds = int(seconds)
        milliseconds = int((seconds - whole_seconds) * 1000)

        hours = whole_seconds // 3600
        minutes = (whole_seconds % 3600) // 60
        seconds = whole_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    @classmethod
    def format_chunk(cls:type[T], chunk: str, index: int) -> str:
        text = chunk['text']
        start, end = chunk['timestamp'][0], chunk['timestamp'][1]
        start_format, end_format = cls.format_seconds(start), cls.format_seconds(end)
        return f"{index}\n{start_format} --> {end_format}\n{text}\n\n"

T = TypeVar('T', bound='VttFormatter')

class VttFormatter:
    @classmethod
    def preamble(cls: type[T]) -> str:
        return "WEBVTT\n\n"

    @classmethod
    def format_seconds(cls: type[T], seconds:int)-> str:
        whole_seconds = int(seconds)
        milliseconds = int((seconds - whole_seconds) * 1000)

        hours = whole_seconds // 3600
        minutes = (whole_seconds % 3600) // 60
        seconds = whole_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    @classmethod
    def format_chunk(cls: type[T], chunk:str, index: int)-> str:
        text = chunk['text']
        start, end = chunk['timestamp'][0], chunk['timestamp'][1]
        start_format, end_format = cls.format_seconds(start), cls.format_seconds(end)
        return f"{index}\n{start_format} --> {end_format}\n{text}\n\n"


def convert(input_path:str, output_format:str, output_dir:str, verbose:bool)-> None:
    with open(input_path) as file:
        data = json.load(file)

    formatter_class = {
        'srt': SrtFormatter,
        'vtt': VttFormatter,
        'txt': TxtFormatter
    }.get(output_format)

    string = formatter_class.preamble()
    for index, chunk in enumerate(data['chunks'], 1):
        entry = formatter_class.format_chunk(chunk, index)

        if verbose:
            print(entry)

        string += entry

    with open(os.path.join(output_dir, f"output.{output_format}"), 
              'w', encoding='utf-8') as file:
        file.write(string)

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert JSON to an output format.")
    parser.add_argument("input_file", help="Input JSON file path")
    parser.add_argument("-f", "--output_format", default="all", 
                        help="Format of the output file (default: srt)", 
                        choices=["txt", "vtt", "srt"])
    parser.add_argument("-o", "--output_dir", default=".", 
                        help="Directory where the output file/s is/are saved")
    parser.add_argument("--verbose", action="store_true",
                         help="Print each VTT entry as it's added")

    args = parser.parse_args()
    convert(args.input_file, args.output_format, args.output_dir, args.verbose)

if __name__ == "__main__":
    # Example Usage:
    # python convert_output.py output.json -f vtt -o /tmp/my/output/dir
    main()
