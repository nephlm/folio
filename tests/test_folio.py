#!/usr/bin/env python
import pytest

import folio.folio as fol

def test_basic():
    assert 1==1

def test_tokenize():
    text = "par1\n\npar2"
    tokens = fol.Folio().tokenize(text)
    assert tokens == [
        {'text': 'par1', 'type': 'paragraph'},
        {'text': 'par2', 'type': 'paragraph'},
    ]


def test_tokenize_fence_block():
    text = "par1\n\n>>>.epilog\nquote par 1\n\n quote par2\n>>>\n\n par 2\n\n"
    tokens = fol.Folio().tokenize(text)
    print(tokens)
    assert tokens == [
        {'type': 'paragraph', 'text': 'par1'}, 
        {'type': 'block_quote_start'}, 
        {'type': 'paragraph', 'text': 'quote par 1'}, 
        {'type': 'paragraph', 'text': ' quote par2'}, 
        {'type': 'block_quote_end'}, 
        {'type': 'paragraph', 'text': ' par 2'}
    ]

@pytest.mark.parametrize('text, style', [
    ('>>>.thing\nFoo\n>>>\n\n', '.thing'),
    ('>>>\nFoo\n>>>\n\n', None),
])
def test_fence_block_regex(text, style):
    pattern = fol.FolioBlockGrammar.block_fence
    m = pattern.match(text)
    assert m.groups() == (style,)
    assert m.group(0) == f'>>>{style if style else ""}\n'
    assert m.group(1) == style

@pytest.mark.skip(reason="not yet")
def test_inline():
    text = "A paragraph with *emphasized* text."
    tokens = fol.Folio().tokenize(text)
    assert tokens == [
        {'text': 'foo', 'type': 'paragraph'}
    ]