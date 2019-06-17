#!/usr/bin/env python

import argparse
import glob
import os
import sys

class Book(object):
    def __init__(self, files):
        self.files = files
        self.book_files = [BookFile(book_file) for book_file in self.files]

    def assemble(self):
        book_text = ''
        first = True
        for book_file in self.book_files:
            if not first:
                book_text += '\n\n<!--SCENE-->\n\n'
            book_text += book_file.get_text()
            first = False
        return book_text

class BookFile(object):
    def __init__(self, book_file):
        self.book_file = book_file

    def get_text(self):
            text = self.book_file.read()
            return text


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("src_path", metavar="path", type=argparse.FileType('r'), nargs='+',
            help=("Path to files to be merged; enclose in quotes, accepts * as "
                    "wildcard for directories or filenames"))
    # parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
    return parser.parse_args()

def main():
    args = parse_args()
    files = args.src_path
    for fi in files:
        print(fi)
    book = Book(files)
    print(book.assemble())




if __name__ == "__main__":
    main()