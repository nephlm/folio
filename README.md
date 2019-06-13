# Folio

An automation system to convert a set of files constructed from a subset of markdown and transform it into a Latex document which can be used to build a pdf suitable for uploading to Amazon et al.

The idea is to have one source for the document and when a change is made be able to generate both the ebook and print book from the same source without having to do any fiddling.

This is for academic articles or dissertations.  It's limited in scope fiction books.  The supported markdown will be extremely limited.  At first probably to:

* headers (atx style (1-6 #))
* span emphasis (italics, bold, etc)
* Links (inline definition only)

Lists are a likely addition but not part of MVP.

Characters that will need special thought about how to represent them in the source material or during the automation/transformation process:

* html: <, &
* markdown: 
* latex: $ % # _ ^ & ~ \ { } and sometimes [ ]

## Metadata

Matched braces inside an html comment (&lt;!--{}--&gt;) will be interpreted as json metadata.

### Meta data elements.

* scope: defaults to 'scene', but can also be set to 'book', 'section' or 'chapter'.  Files are assumed to be individual scenes.
* h1_scale: Normally the same as scope.  When the markdown files are concatenated any headings are adjusted based on this scale.  All headings of 'section' scale add one to their level so an H1 becomes an H2 and and H3 becomes an H4.  Similarly chapter scale add 2 and scene scale add 3.  This allows each file to be normally scoped with the highest level heading (H1), but the compiled document has a consistent hierarchy.  

* author: The name of the author of the scoped work.



