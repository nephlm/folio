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

## Requirements

This list will likely grow.

* This is built on top of the LaTeX novel package, so it's required as well as a version of LaTeX that can run it (2016+).
* The ability run python.
    * This probably effectively means a linux environment (Mac?).  I hear the Windows 10 will start shipping with linux soon, but I don't know what that means.

## Components

* *Assembler*: Collect the .md files that are part of the book.  Process and assemble them into a single .md file.
    * Will include some header re-writing.  Ideally there will be an .md file parser library, but it might be done with simple regexes instead.  
    * Inserting file level metadata at the point where files are joined. (see below) This will inserted as LaTeX comments so it should be ignored.
    * `<!--SCENE-->` will also be added at each file join point.
    * Files do not need to contain text, they may be all metadata. For example there might be a book or section level metadata file, that contains no prose.
* *Translator*: Take the output of File Collector and translate it into LaTex.
    * Find LaTeX reserved/special characters and escape them.
    * Apply appropriate latex commands to create emphasis, et al.  
    * Construct front matter and chapter headers.
    * Output the LaTeX source.
* *Control*
    * Will run the above two components as well as the LaTeX command to compile into a PDF file. 

## Metadata

Matched braces inside an html comment (&lt;!--{}--&gt;) will be interpreted as json metadata.

Maybe instead of JSON have this be lines starting with LaTeX comment character (%)  with a form:
```
% key: value
```
Would not handle nesting well at all.  Probably fine for most usages, but would break down at the book level without some sort of compound keys.

```
% credit_1: cover design; Joe Artist; joeartist.com
```

Pretty unfriendly, but then so is JSON for this sort of thing if you're hand typing it.

### Meta data elements.

* **scope**: defaults to 'scene', but can also be set to 'book', 'section' or 'chapter'.  Files are assumed to be individual scenes.  A section is a collection of chapters within one physical book.  These are often confusingly called books.  MVP likely will not 
* **h1_scale_offset**: This how many levels each heading should be shifted down.  If this is set to 2, than an H1 will become an H3 and a H3 will become an H5.  By default if the scope is 'book' this is set to 0, 'section' sets this to 1, 'chapter' sets it to 2 and 'scene' sets it to 3.  This allows each file to be normally scoped with the highest level heading (H1), but the compiled document has a consistent hierarchy.  
* **author**: The name of the author of the scoped work.
* **title**: 
    * If there is a top level (H1) header, will use the content of the that.
    * If no H1 defaults to the name of the file, with .md extension removed.  If there is a __ in the filename, whatever precedes the __ will be dropped.  This allows files to be ordered by what precedes the the __ and can still extract the section title that should be used.
* **subtitle**: Subtitle of the section.  (Should it be extracted from H2?)
* **epigraph**: Extract from H3?  JSON multiline is not super author friendly.  Needs more though.
* Book level only: The following metadata is only valid at book scope.  It will be ignored at other scopes.
    * publisher
    * publisher_url
    * ISBN: Can be a string or a dict with edition names (ebook, paperback, etc) as keys.
    * copyright_holder: defaults to author.
    * copyright_year: defaults to the current year.
    * disclaimer: path to a text or md file.  Overrides default on copyright page.
    * rights path to a text or md file.  Overrides default on copyright page.
    * title_page: I don't know what to do about this.  For the moment this is a place holder for future development.  Maybe links to some images or something. 
    * credits: A list of tuples `(thing, person, url)`.  For example `[['cover design', 'Joe Artist', 'joeswebsite.com']]`.  You can even thank me.

Title pages can be arbitrarily complicated and I don't have the required metadata so support a flexible solution except for having the author write LaTex (no.)  Think more about this issue.

