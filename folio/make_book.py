#!/usr/bin/env python

import argparse


import folio 
import latex_renderer 

def get_files(args):
    if isinstance(args.files, str):
        return [args.files]
    else:
        return args.files

def scan_for_title_and_author(tokens):
    title = None
    author = None
    for token in tokens:
        if token['type'] == 'metadata':
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
            renderer = latex_renderer.Renderer()
            parser = folio.Folio(renderer=renderer)
            tokens = parser.tokenize(text)
            title, author = scan_for_title_and_author(tokens)
            renderer.title = title
            renderer.author = author
            output = parser.render_tokens(tokens)
            print(output)
    
# def block_parse(text):
#     tokens = folio.Folio().tokenize(text)
#     #tokens = []
#     print(tokens)
#     return tokens

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files')
    args = parser.parse_args()

    path_list = get_files(args)
    process_files(path_list)        


if __name__ == "__main__":
    main()