# Makefile for cv
DATADIR=data
SRCDIR=src
TMP=temp
PDF=$(DATADIR)/$(TMP).pdf
TEXDIR=tex
OUT=output

local:
	cd $(SRCDIR); ./get_cv.py && open ../$(PDF)

all:
	make update
	make index
	make readme
	open $(PDF)

update:
	cd $(SRCDIR); ./get_cv.py --update

parse:
	cd $(SRCDIR); ./get_cv.py --parse

compact:
	cd $(SRCDIR); ./get_cv.py --compact

index:
	cd $(DATADIR); pandoc -s --metadata title="CV" -i $(TMP).tex -f latex -t html -o ../$(OUT)/index.html

readme:
	cd $(DATADIR); pandoc -s -i $(TMP).tex -f latex -t gfm -o ../$(OUT)/README.md

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
