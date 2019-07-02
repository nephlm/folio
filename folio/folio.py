#!/usr/bin/env python

import re

import mistune

print(dir(mistune))

class FolioBlockGrammar(mistune.BlockGrammar):

    block_fence = re.compile(r'^>>>(\..*)?\n')

class FolioBlockLexer(mistune.BlockLexer):

    grammar_class = FolioBlockGrammar

    def __init__(self, rules=None, **kwargs):
        self.default_rules.insert(4, 'block_fence')
        super().__init__(rules, **kwargs)
        self._in_block_fence = False

    def parse_block_fence(self, m):
        name = m.group(1) if m.group(1) else None
        print(name)
        if  self._in_block_fence:
            self._in_block_fence = False
            self._blockquote_depth -= 1
            self.tokens.append({'type': 'block_quote_end'})
        else:
            self.tokens.append({'type': 'block_quote_start', 'name': name})
            self._blockquote_depth += 1
            self._in_block_fence = True


class Folio(mistune.Markdown):

    def __init__(self, renderer=None, inline=None, block=None, **kwargs):
        if block is None:
            block = FolioBlockLexer()
        super().__init__(renderer, inline, block, **kwargs)

    def tokenize(self, text, rules=None):
        self.tokens = self.block(mistune.preprocessing(text), rules)
        return self.tokens
