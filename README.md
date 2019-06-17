# Folio

An automation system to convert a set of files constructed from a subset of markdown and transform it into a Latex document which can be used to build a pdf suitable for uploading to Amazon et al.

The idea is to have one source for the document and when a change is made be able to generate both the ebook and print book from the same source without having to do any fiddling.

This is no for academic articles or dissertations.  It's limited in scope popular fiction books.  

## Considerations

Desing goals and considerations for this project. 

### Supported Markdown

The supported markdown will be extremely limited.  At first probably limited to:

* headers (atx style (1-6 #))
* span emphasis (italics, bold, etc)
* Links 
    * Inline definition only 
    * Do I need this?  This is for making PDF to send to POD services, by definition it won't be clickable.  I guess it will create a clickable link in a PDF, but that isn't use case we're trying to solve for.  
    * However ultimately we'd like one build system that will build the POD pdf as well as the .mobi (epub, etc) ebook and those will have clickable links.
* Lists are a likely addition but not part of MVP.
* block quotes are also likely additions, but not part of the initial MVP.

### Special Characters

Characters that will need special thought about how to represent them in the source material or during the automation/transformation process:

* html: <, &
* markdown: 
* latex: $ % # _ ^ & ~ \ { } and sometimes [ ]

I thik we can start folio commands with `;;` at the start of the line.  Any foio list commands will be additive single lines.

```
;; credit "Cover design" "Joe Artist" "https://joeartist.com"
;; credit "Interior design" "Folio"  "https://nephlm.github.com/folio"
```

## Requirements

This list will likely grow.

* This is built on top of the LaTeX novel package, so it's required as well as a version of LaTeX that can run it (2016+).
* The ability run python.
    * This probably effectively means a linux environment (Mac?).  I hear the Windows 10 will start shipping with linux soon, but I don't know what that means.

## Supported Grammar

The starting point is markdown so it should be familiar with markdown.  However it will be a stripped down version of markdown, certainly for MVP.  However there are required features not supported by markdown.  As I use [tiddlywiki](https://tiddlywiki.com/), their markdown inspired [WikiText](https://tiddlywiki.com/static/WikiText.html) will be my goto source for grammar extensions.

### Inline Grammars

Inline grammars don't span paragraphs or other block elements.

* emphasis - Rendered as italics.  (Some \**emphasized*\* text).  Underscores can also be used.
* strong - Rendered as bold.  (Some \*\***bolded**\*\* text).  Underscores can also be used.
* inline comments - Not rendered.  (Some <!-- commented --> text). 
    * (Some &lt;!-- commented --> text)
* strikethrough - I'm a fan of this being a first class formatting, but I'm not sure it  has much purpose in this context.  Some ~~strikethrough~~ text.
* monospace - Rendered in a monospace font (some `monospace` text)  
* superscript - I feel like these should be included but are not part of stock markdown.  If we were rendering to HTML we could just use &lt;sup> or &lt;sub>, but we aren't.  WikiText uses ^^superscript^^ and ,,subscript,,.
* subscript - See superscript above.
* emdash - -- will be rendered as an emdash
* quotes - Straight quotes will be rendered as typographical quotes.
* ellipses - Three periods will be rendered as typographical ellipses

### Block Grammars

* Paragraph - The paragraph is the basic block in folio.  Paragraphs are separated by one or more empty lines.  Empty lines are any line containing only zero or more whitespace characters.
* Blockquotes - Blockquotes begin with a line a line beginning with three &lt; and end with another line beginning with three &lt;.
    * class - Immediately following the &lt;&lt;&lt; a class can be added.  This is generally for a special block quote that is to be used in frontmatter of a chapter header. 
        * Currently defined special classes:
            * epigram - If defined as part of front matter will be put on it's own page in the front matter.  If part of a chapter head, will be put there, otherwise it's ignored.
    * source - Any text on the closing &lt;&lt;&lt; line will be interpreted as the source for the blockquote or epigram and will be rendered as such. 
* bookfrontmatter - 
* chapterfrontmatter - 

### For Later

* Lists

### For Never (Probably)

* Tables

## Components

The parser/renderer architecture can hopefully be built on top of the [mistune](https://github.com/lepture/mistune) markdown parser.  It will likely have to be heavily modified (hopefully as a subclass, rather than a fork) to deal with the above grammar.

* *Parser*: Collect the .md files that are part of the book.  
    * Ordering of files
        * In general alphabetical of full path.
        * `Frontmatter.md` and `Backmatter.md` move to the front or end of the order on a per directory basis. 
    * Can I process each file individually or do they have to be assembled first?
        * Really try to treat them as separate.
    * Will include some header re-writing.  
    * Files do not need to contain text, they may be all metadata. For example there might be a book or section level metadata file, that contains no prose.
* *Renderer*: 
    * Should be module enough so we can also make both a LaTeX and ebook renderer
    * LaTeX
        * Take the output of File Parser and render it into LaTex.
        * Find LaTeX reserved/special characters and escape them.
        * Apply appropriate latex commands to create emphasis, et al.  
        * Construct front matter and chapter headers.
        * Output the LaTeX source.
    * Mobi, epub, etc.
* *Control*
    * Will run the above two components as well as the LaTeX command to compile into a PDF or ebook file. 

## Metadata

Folio commands begin with `;;` at the beginning of the line.  All parts of the command must be on a single line. 

### Commands

Commands are generally removed or transformed before LaTeX generation.  

#### scope

Basically the same as the set, but elevated due to importance.

defaults to 'scene', but can also be set to 'book', 'section' or 'chapter'.  Files are assumed to be individual scenes.  A section is a collection of chapters within one physical book.  These are often confusingly called books.  MVP likely will not deal with sections.

```
;; scope chapter
```

#### set

```
;; set title "Great American Novel"
```

Values that can be set.  Set always overwrites a previous value.  

* **h1_scale_offset**: This how many levels each heading should be shifted down.  If this is set to 2, than an H1 will become an H3 and a H3 will become an H5.  By default if the scope is 'book' this is set to 0, 'section' sets this to 1, 'chapter' sets it to 2 and 'scene' sets it to 3.  This allows each file to be normally scoped with the highest level heading (H1), but the compiled document has a consistent hierarchy.  
* **author**: The name of the author of the scoped work.
* **title**: 
    * If there is a top level (H1) header, will use the content of the that.
    * If no H1 defaults to the name of the file, with .md extension removed.  If there is a __ in the filename, whatever precedes the __ will be dropped.  This allows files to be ordered by what precedes the the __ and can still extract the section title that should be used.
* **subtitle**: Subtitle of the section.  (Should it be extracted from H2?)
* **epigraph**: Extract from H3?  Command multiline doesn't exist.  How do you know when H3 ends?  Epigraph as custom style?  That would solve a lot of the problems.  Would have a start/end and wouldn't make headings semantic.

Values that should probably only be set once.

* publisher
* publisher_url
* copyright_holder: defaults to author.
* copyright_year: defaults to the current year.
* disclaimer: path to a text or md file.  Overrides default on copyright page.
* rights path to a text or md file.  Overrides default on copyright page.
* title_page: I don't know what to do about this.  For the moment this is a place holder for future development.  Maybe links to some images or something. 

Unknown values will be silently processed.  

#### lists

Stores a list of tupeles.

```
;; list credits "Cover design" "Joe Artist" "https://joeartist.com"
;; list credits "Interior art: "Jane Artist" "https://janeartist.com"
;; list ISBN paperback "bunch of nubmers" 
;; list ISBN ebook "bunch of nubmers" 
```

Tuple names known by folio:

    * credits: A list of tuples `(thing, person, url)`.  For example `[['cover design', 'Joe Artist', 'joeswebsite.com']]`.  You can even thank me.
    * ISBN: Can be a string or a dict with edition names (ebook, paperback, etc) as keys.

Title pages can be arbitrarily complicated and I don't have the required metadata so support a flexible solution except for having the author write LaTex (no.)  Think more about this issue.

