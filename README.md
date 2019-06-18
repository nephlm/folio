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
* TitlePages - Title pages can be arbitrarily complicated and I don't have the required metadata so support a flexible solution except for having the author write LaTex (no.)  Think more about this issue.





### Book Structures

Folio recognizes three levels of hierarchy in a book.

* Book - A single physical book.
* Section - A group of chapters.   Won't likely be supported by MVP.
    * These are often used to designate a large passage of time between parts of the novel.
    * 
* Chapter - A group of scenes.

To start these structures a structure block needs to be created which instructs Folio to render the appropriate beginning.  Each block requires certain metadata about the structure.

The start structure block begins and ends with `@@`.  After the starting `@@` a marker designating what sort of section should be started is required.  This means the starting marker will be one of these three:

* `@@.book`
* `@@.section`
* `@@.chapter`

Regardless of how it starts it ends with an `@@`.  The starting and ending markers should be on line by themselves with no spaces before them.

Between the start and end marker are mostly data declarations.  Declarations begin with `;;` and are of the form `;;key=value`.  They are one per line with no spaces before the `;;`  The value may have spaces but no multiline values.  

There are some keys which may contain multiple values (ISBN, credits, etc), in such case they are designated as `;;key['selector'] = value`

Multiline data bay also be entered in form of a named blockquote (see above).

```
<<<.epigraph
Line1
Line2
<<<
```

Folio will interpret that as something similar to `;;epigraph=Line1\nLine2`.  Be aware that there are limited fields that will accept multiline data.  Unless specified otherwise assume multiline data will not be accepted. 

#### Book

A book is started by a book start structure.  

The book structure bock will use the following data declarations:

* title
* subtitle
* author
* epigraph - multiline
* publisher
* publisher_url
* copyright_holder: defaults to author.
* copyright_year: defaults to the current year.
* disclaimer: Multiline and optional.  Overrides default on copyright page.
* rights: Multiline and optional.  Overrides default on copyright page.
* title_page: I don't know what to do about this.  For the moment this is a place holder for future development.  Title pages are arbitrarily complicated.  We'll have to figure something out as we go.
* credits: Multivalue and optional.  
* isbn: Multivalue and optional.

A minimal book start structure looks like this:

```
@@.book
;;title=My Awesome book
;;author=Nephlm Smith
@@
```
In general publisher data is highly recommended.

#### Section

A section is started by a section start structure.  At present this does not render as anything.

Sections support the following data declarations:

* title
* subtitle
* epigraph

Minimal section start declaration looks like this:

```
@@.section
;;title=Before the War
@@
```

#### Chapter

A section is started by a section start structure.  At present this does not render as anything.

Sections support the following data declarations:

* title
* subtitle
* epigraph

Minimal section start declaration looks like this:

```
@@.chapter
;;title=Before the War
@@
```

Chapters have a special shortcut if there is no subtitle or epigraph.  Any H1 header will be considered to a chapter start with the value of the heading equal to the header text.

The below is equivalent to the above minimal example. 

```
# Before the War
```




#### Simplified Complete Book Example

```

@@.book
;;title=Title of the Book
;;subtitle=It's Awesome, Buy It!
;;author=Joe author
;;isbn["ebook"] = <bunch of numbers>
;;credits['Cover design']=Joe Artist
;;credit_urls['Cover design]=https://joeartist.com
@@

@@.section
;;title = Title of the section
@@

# Chapter 1

Lorem Ipsum etc etc ...

@@.chapter
;;title=Chapter 2
;;subtitle=The Sub-Title of the Chapter

<<<.epigraph
In the beginning there was stuff
<<< someone else


<!--.notes
Notes about what happen in the chapter
-->
@@

Lorem Ipsum etc etc ...

@@.backmatter
<<<.about_the_author
Stuff about me
<<<
@@
```


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

