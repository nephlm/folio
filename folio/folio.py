#!/usr/bin/env python

import re

import mistune
import latex_renderer

class FolioBlockGrammar(mistune.BlockGrammar):

    block_fence = re.compile(r'^>>>(\..*)?\n')
    section_fence = re.compile(r'^@@(\..*)?\n')
    metadata = re.compile(r'^;;\s*(\w+)\s*=\s*(.+)')
    block_comment = re.compile(r"^'''(.*?)'''\n+", re.S)

class FolioBlockLexer(mistune.BlockLexer):

    grammar_class = FolioBlockGrammar

    def __init__(self, rules=None, **kwargs):
        self.default_rules.insert(1, 'block_comment')
        self.default_rules.insert(4, 'block_fence')
        self.default_rules.insert(5, 'section_fence')
        self.default_rules.insert(6, 'metadata')
        super().__init__(rules, **kwargs)
        self._in_block_fence = False
        self._in_section_fence = False

    def parse_block_fence(self, m):
        name = m.group(1) if m.group(1) else None
        if  self._in_block_fence:
            self._in_block_fence = False
            self._blockquote_depth -= 1
            self.tokens.append({'type': 'block_quote_end'})
        else:
            self.tokens.append({'type': 'block_quote_start', 'name': name})
            self._blockquote_depth += 1
            self._in_block_fence = True

    def parse_block_comment(self, m):
        # Comments are dropped at this stage they are for the author not the finished book
        print('found a comment')
        print(m.groups())
        print(m.group(1))
        pass

    def parse_section_fence(self, m):
        name = m.group(1) if m.group(1) else None
        if  self._in_section_fence:
            self._in_section_fence = False
            self.tokens.append({'type': 'section_header_render'})
        else:
            self.tokens.append({'type': 'section_header_start', 'level': name})
            self._in_section_fence = True

    def parse_metadata(self, m):
        key = m.group(1)
        val = m.group(2)
        self.tokens.append({'type': 'metadata', 'key': key, 'val': val})

class Folio(mistune.Markdown):

    def __init__(self, renderer=None, inline=None, block=None, **kwargs):
        if block is None:
            block = FolioBlockLexer()
        if renderer is None:
            renderer = latex_renderer.Renderer()
        super().__init__(renderer, inline, block, **kwargs)

    def tokenize(self, text, rules=None):
        self.tokens = self.block(mistune.preprocessing(text), rules)
        self.tokens.reverse()
        print(self.tokens)
        return self.tokens

    def render_tokens(self, tokens):
        out = self.renderer.placeholder()
        while self.pop():
            out += self.tok()
        return out

