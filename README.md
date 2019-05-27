# Folio

An automation system to convert a set of files constructed from a subset of markdown and transform it into a Latex document which can be used to build a pdf suitable for uploading to Amazon et al.

The idea is to have one source for the document and when a change is made be able to generate both the ebook and print book from the same source without having to do any fiddling.

This is for academic articles or dissertations.  It's limited in scope fiction books.  The supported markdown will be extremely limited.  At first probably to:

* headers (atx style (1-6 #))
* span emphasis (italics, bold, etc)
* Links (inline definition only)

Lists are a likely additionm but not part of MVP.

Charactes that will need special thought about how to represent them in the source material or during the automation/transformation process:

* html: <, &
* markdown: 
* latex: %, \, $
