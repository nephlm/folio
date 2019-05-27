# install the texlive package

Requires latex-live 2016+, the version that is shipped with 

```
apt install texlive-latex-extra  # may already be installed.
apt install xzdec
tlmgr init-usertree
tlmgr option repository ftp://tug.org/historic/systems/texlive/2015/tlnet-final 

```


# Compiling a document

```
pdflatex hello-world.tex
```