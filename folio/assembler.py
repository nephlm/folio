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
        for book_file in self.book_files:
            book_text += book_file.get_text()
        return book_text

class BookFile(object):
    def __init__(self, book_file):
        self.book_file = book_file

    def get_text(self):
        with open(self.book_file) as fp:
            text = fp.read()
            return text


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("src_path", metavar="path", type=str,
            help=("Path to files to be merged; enclose in quotes, accepts * as "
                    "wildcard for directories or filenames"))
    return parser.parse_args()

def main():
    args = parse_args()
    files = sorted(glob.glob(args.src_path))
    book = Book(files)
    print(book.assemble())




if __name__ == "__main__":
    main()