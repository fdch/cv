# Makefile for cv
DATADIR=data
SRCDIR=src
TMP=temp
TEXDIR=tex
OUT=output
TITLE="Federico Cámara Halac"
PDCFLAGS=-s --metadata title=$(TITLE) --css style/style.css
MAIN=main.py
PY=/usr/local/bin/python3
CC=$(PY) $(SRCDIR)/$(MAIN)
PDF=$(DATADIR)/$(TMP).pdf

help:
	$(CC) -h
	@echo "See the Makefile for more info"

local:
	make cv && open $(PDF) 

all:
	make update
	make cv
	make release
	make references

references:
	if [[ ! "$(refselect)" ]]; then \
			$(CC) --references --datadir=$(DATADIR); \
	else \
		echo $(refselect); \
		$(CC) --references --datadir=$(DATADIR) --refselect="$(refselect)"; \
	fi \
	&& open $(DATADIR)/references.pdf

cv:
	$(CC) --cv 	--datadir=$(DATADIR) && open $(PDF)

update:
	$(CC) --update --datadir=$(DATADIR)

parse:
	$(CC) --parse --datadir=$(DATADIR)

compact:
	$(CC) --compact --cv --datadir=$(DATADIR)

release:
	cd $(DATADIR); pandoc $(PDCFLAGS) -i $(TMP).tex -f latex -t html -o ../index.html
	pandoc -i index.html -f html -t gfm -o README.md
	pandoc -i index.html -f html -t docx -o $(OUT)/cv.docx

project:
	rm $(DATADIR)/project.zip
	cd $(TEXDIR); zip ../$(DATADIR)/project.zip *

pdf:
	cd $(DATADIR); pdflatex --interaction=nonstopmode $(TMP).tex
	open $(PDF)

new:
	cp $(PDF) $(OUT)/temp-new.pdf
	cp $(DATADIR)/$(TMP).tex $(OUT)/temp-new.tex
# 	cp $(DATADIR)/res.cls $(OUT)

push:
	git add . 
	git commit 
	git push

cover:
	if [[ ! "$(call)" ]]; then \
		echo "USAGE: make cover call='path/to/universityname.py'"; \
	else \
		$(CC) --cover=$(call); \
	fi

.PHONY: cover all new