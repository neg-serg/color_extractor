#!/usr/bin/pypy3

from colorthief import ColorThief as ctf
from pathlib import Path  # get corrent path
import subprocess
import multiprocessing as mp
import os
from os.path import expanduser
import sys


class Extractor():
    def __init__(self, directory, color_count=8, quality=320):
        self.color_count = color_count
        self.quality = quality
        search_dir = os.path.realpath(expanduser(directory))
        if Path(os.path.normpath(search_dir)).is_dir():
            self.directory = search_dir
        else:
            sys.exit(0)
        self.print_filename = True

    def rgb_to_24bit(self, rgb):
        return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m  \033[49m" + \
            f" #{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x} "

    def rgb_to_24bit_fancy(self, rgb):
        return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m  \033[49m" + \
            f" #{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x} "

    def rgb2hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def load_filelist_from_dir(self):
        return subprocess.check_output(
            ['find', self.directory, '-type', 'f']
        ).decode('UTF-8').split('\n')

    def process_picture(self, pic):
        filename = os.path.normpath(os.path.realpath(expanduser(pic)))
        if Path(filename).exists():
            try:
                color_thief = ctf(expanduser(pic))
                gen_palette = color_thief.get_palette(
                    color_count=self.color_count, quality=self.quality
                )
            except Exception:
                return
            printer = self.rgb_to_24bit
            for t in map(printer, gen_palette):
                print(t, end='')
            if self.print_filename:
                print(f'    {pic}', end='')
            print()

    def extract_pallete(self):
        pool = mp.Pool(processes=8)
        pool.map(
            self.process_picture, self.load_filelist_from_dir()
        )


if __name__ == '__main__':
    extractor = Extractor('~/pic/wl')
    extractor.extract_pallete()

