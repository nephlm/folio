#!/usr/bin/env python

import argparse


import folio.folio as Folio
import folio.latex_renderer as renderer

def get_files(args):
    if isinstance(args.files, str):
        return [args.files]
    else:
        return args.files

def scan_for_title_and_author(tokens):
    title = None
    author = None
    for token in tokens:
        if token['type'] == 'metada':
            if token['key'] == 'title' and title is None:
                title = token['val'] 
                if author:
                    break
            elif token['key'] == 'author' and author is None:
                author = token['val']
                if title:
                    break
    return title, author

def process_files(path_list):
    for path in path_list:
        with open(path, 'r') as fp:
            text = fp.read()
            tokens = block_parse(text)
            title, author = scan_for_title_and_author(tokens)
    
def block_parse(text):
    tokens = []
    return tokens

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files')
    args = parser.parse_args()

    path_list = get_files(args)
    process_files(path_list)        


if __name__ == "__main__":
    main()