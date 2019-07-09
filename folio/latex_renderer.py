import re

def escape(text, quote=None, smart_amp=None):
    return text

def escape_link(url):
    return url

class Renderer(object):
    """The default HTML renderer for rendering Markdown.
    """

    def __init__(self, title, author, **kwargs):
        self.title = title
        self.author = author
        self.options = kwargs
        self.metadata = {'.book': {}, '.section': {}, '.chapter': {}}
        self.section_number = 0
        self.chapter_number = 0

    def clear_metadata(self, level):
        if level not in self.metadata:
            raise ValueError(f'Unknown book structure {level} (must be .book, .section or .chapter')
        self.metadata[level] = {}

    def add_metadata(self, level, key, val):
        if level not in self.metadata:
            raise ValueError(f'Unknown book structure {level} (must be .book, .section or .chapter')
        self.metadata[level][key] = val

    def increment_section(self):
        self.section_number += 1

    def increment_chapter(self):
        self.chapter_number += 1

    def placeholder(self):
        """Returns the default, empty output value for the renderer.

        All renderer methods use the '+=' operator to append to this value.
        Default is a string so rendering HTML can build up a result string with
        the rendered Markdown.

        Can be overridden by Renderer subclasses to be types like an empty
        list, allowing the renderer to create a tree-like structure to
        represent the document (which can then be reprocessed later into a
        separate format like docx or pdf).
        """
        return []

    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        raise NotImplementedError('block_code isn\'t implemented yet')

    def block_quote(self, text):
        """Rendering <blockquote> with the given text.

        :param text: text content of the blockquote.
        """
        raise NotImplementedError('block_quote isn\'t implemented yet')

    def block_html(self, html):
        """Rendering block level pure html content.

        :param html: text content of the html snippet.
        """
        raise NotImplementedError('not implemented yet')
        if self.options.get('skip_style') and \
           html.lower().startswith('<style'):
            return ''
        if self.options.get('escape'):
            return escape(html)
        return html

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        raise NotImplementedError('not implemented yet')
        return '<h%d>%s</h%d>\n' % (level, text, level)

    def hrule(self):
        """Rendering method for ``<hr>`` tag."""
        raise NotImplementedError('not implemented yet')
        if self.options.get('use_xhtml'):
            return '<hr />\n'
        return '<hr>\n'

    def list(self, body, ordered=True):
        """Rendering list tags like ``<ul>`` and ``<ol>``.

        :param body: body contents of the list.
        :param ordered: whether this list is ordered or not.
        """
        raise NotImplementedError('not implemented yet')
        tag = 'ul'
        if ordered:
            tag = 'ol'
        return '<%s>\n%s</%s>\n' % (tag, body, tag)

    def list_item(self, text):
        """Rendering list item snippet. Like ``<li>``."""
        raise NotImplementedError('not implemented yet')
        return '<li>%s</li>\n' % text

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        raise NotImplementedError('not implemented yet')
        return '<p>%s</p>\n' % text.strip(' ')

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.

        :param header: header part of the table.
        :param body: body part of the table.
        """
        raise NotImplementedError('not implemented yet')
        return (
            '<table>\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)

    def table_row(self, content):
        """Rendering a table row. Like ``<tr>``.

        :param content: content of current table row.
        """
        raise NotImplementedError('not implemented yet')
        return '<tr>\n%s</tr>\n' % content

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.

        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        raise NotImplementedError('not implemented yet')
        if flags['header']:
            tag = 'th'
        else:
            tag = 'td'
        align = flags['align']
        if not align:
            return '<%s>%s</%s>\n' % (tag, content, tag)
        return '<%s style="text-align:%s">%s</%s>\n' % (
            tag, align, content, tag
        )

    def double_emphasis(self, text):
        """Rendering **strong** text.

        :param text: text content for emphasis.
        """
        raise NotImplementedError('not implemented yet')
        return '<strong>%s</strong>' % text

    def emphasis(self, text):
        """Rendering *emphasis* text.

        :param text: text content for emphasis.
        """
        raise NotImplementedError('not implemented yet')
        return '<em>%s</em>' % text

    def codespan(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """
        raise NotImplementedError('not implemented yet')
        text = escape(text.rstrip(), smart_amp=False)
        return '<code>%s</code>' % text

    def linebreak(self):
        """Rendering line break like ``<br>``."""
        raise NotImplementedError('not implemented yet')
        if self.options.get('use_xhtml'):
            return '<br />\n'
        return '<br>\n'

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text.

        :param text: text content for strikethrough.
        """
        raise NotImplementedError('not implemented yet')
        return '<del>%s</del>' % text

    def text(self, text):
        """Rendering unformatted text.

        :param text: text content.
        """
        raise NotImplementedError('not implemented yet')
        if self.options.get('parse_block_html'):
            return text
        return escape(text)

    def escape(self, text):
        """Rendering escape sequence.

        :param text: text content.
        """
        raise NotImplementedError('not implemented yet')
        return escape(text)

    def autolink(self, link, is_email=False):
        """Rendering a given link or email address.

        :param link: link content or email address.
        :param is_email: whether this is an email or not.
        """
        raise NotImplementedError('not implemented yet')
        text = link = escape_link(link)
        if is_email:
            link = 'mailto:%s' % link
        return '<a href="%s">%s</a>' % (link, text)

    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        raise NotImplementedError('not implemented yet')
        link = escape_link(link)
        if not title:
            return '<a href="%s">%s</a>' % (link, text)
        title = escape(title, quote=True)
        return '<a href="%s" title="%s">%s</a>' % (link, title, text)

    def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        raise NotImplementedError('not implemented yet')
        src = escape_link(src)
        text = escape(text, quote=True)
        if title:
            title = escape(title, quote=True)
            html = '<img src="%s" alt="%s" title="%s"' % (src, text, title)
        else:
            html = '<img src="%s" alt="%s"' % (src, text)
        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html

    def inline_html(self, html):
        """Rendering span level pure html content.

        :param html: text content of the html snippet.
        """
        raise NotImplementedError('not implemented yet')
        if self.options.get('escape'):
            return escape(html)
        return html

    def newline(self):
        """Rendering newline element."""
        raise NotImplementedError('not implemented yet')
        return ''

    def footnote_ref(self, key, index):
        """Rendering the ref anchor of a footnote.

        :param key: identity key for the footnote.
        :param index: the index count of current footnote.
        """
        raise NotImplementedError('not implemented yet')
        html = (
            '<sup class="footnote-ref" id="fnref-%s">'
            '<a href="#fn-%s">%d</a></sup>'
        ) % (escape(key), escape(key), index)
        return html

    def footnote_item(self, key, text):
        """Rendering a footnote item.

        :param key: identity key for the footnote.
        :param text: text content of the footnote.
        """
        raise NotImplementedError('not implemented yet')
        back = (
            '<a href="#fnref-%s" class="footnote">&#8617;</a>'
        ) % escape(key)
        text = text.rstrip()
        if text.endswith('</p>'):
            text = re.sub(r'<\/p>$', r'%s</p>' % back, text)
        else:
            text = '%s<p>%s</p>' % (text, back)
        html = '<li id="fn-%s">%s</li>\n' % (escape(key), text)
        return html

    def footnotes(self, text):
        """Wrapper for all footnotes.

        :param text: contents of all footnotes.
        """
        raise NotImplementedError('not implemented yet')
        html = '<div class="footnotes">\n%s<ol>%s</ol>\n</div>\n'
        return html % (self.hrule(), text)
