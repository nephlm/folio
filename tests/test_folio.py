#!/usr/bin/env python
import pytest

import folio.folio as fol

def test_tokenize():
    text = "par1\n\npar2"
    tokens = fol.Folio().tokenize(text)
    assert tokens == [
        {'text': 'par1', 'type': 'paragraph'},
        {'text': 'par2', 'type': 'paragraph'},
    ]


def test_tokenize_fence_block():
    text = "par1\n\n>>>.epilogue\nquote par 1\n\n quote par2\n>>>\n\n par 2\n\n"
    tokens = fol.Folio().tokenize(text)
    print(tokens)
    assert tokens == [
        {'type': 'paragraph', 'text': 'par1'}, 
        {'type': 'block_quote_start', 'name': '.epilogue'}, 
        {'type': 'paragraph', 'text': 'quote par 1'}, 
        {'type': 'paragraph', 'text': ' quote par2'}, 
        {'type': 'block_quote_end'}, 
        {'type': 'paragraph', 'text': ' par 2'}
    ]


def test_tokenize_section_block():
    text = "par1\n\n@@.book\n;;key1=var1\n\n;;key2=var2\n\n@@\n\n par 2\n\n"
    tokens = fol.Folio().tokenize(text)
    print(tokens)
    assert tokens == [
        {'type': 'paragraph', 'text': 'par1'}, 
        {'type': 'section_header_start', 'level': '.book'}, 
        {'type': 'metadata', 'key': 'key1', 'val': 'var1'}, 
        {'type': 'newline'},
        {'type': 'metadata', 'key': 'key2', 'val': 'var2'}, 
        {'type': 'newline'},
        {'type': 'section_header_render'}, 
        {'type': 'paragraph', 'text': ' par 2'}
    ]


@pytest.mark.parametrize('text, key, val', [
    (';; key1=val1', 'key1', 'val1'),
    (';;key1=val1', 'key1', 'val1'),
    (';;key1=val1\notherstuff', 'key1', 'val1'),
])
def test_metadata_regex(text, key, val):
    pattern = fol.FolioBlockGrammar.metadata
    m = pattern.match(text)
    assert m.groups() ==(key, val)
    assert m.group(1) == key
    assert m.group(2) == val


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