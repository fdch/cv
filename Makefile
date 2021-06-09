# Makefile for cv
DATADIR=data
SRCDIR=src
TMP=temp
PDF=$(DATADIR)/$(TMP).pdf
TEXDIR=tex
OUT=output
TITLE="Federico Cámara Halac"
PDCFLAGS=-s --metadata title=$(TITLE) --css style/style.css

local:
	cd $(SRCDIR); ./get_cv.py && open ../$(PDF)

all:
	make update
	make release
	open $(PDF)

update:
	cd $(SRCDIR); ./get_cv.py --update

parse:
	cd $(SRCDIR); ./get_cv.py --parse

compact:
	cd $(SRCDIR); ./get_cv.py --compact

release:
	cd $(DATADIR); pandoc $(PDCFLAGS) -i $(TMP).tex -f latex -t html -o ../index.html
	pandoc -i index.html -f html -t gfm -o README.md

project:
	rm $(DATADIR)/project.zip
	cd $(TEXDIR); zip ../$(DATADIR)/project.zip *

pdf:
	cd $(DATADIR); pdflatex --interaction=nonstopmode $(TMP).tex
	open $(PDF)

new:
	cp $(PDF) $(OUT)/temp-new.pdf
	cp $(DATADIR)/$(TMP).tex $(OUT)/temp-new.tex
	cp $(DATADIR)/res.cls $(OUT)

push:
	git add . 
	git commit 
	git push
