# Makefile for cv
DATADIR=data
SRCDIR=src
TMP=temp
TEXDIR=tex
OUT=output
TITLE="Federico Cámara Halac"
PDCFLAGS=-s --metadata title=$(TITLE) --css style/style.css --resource-path=$(DATADIR)
MAIN=main.py
PY=/usr/local/bin/python3
CC=$(PY) $(SRCDIR)/$(MAIN)
PDF=$(DATADIR)/$(TMP).pdf
JOIN=/System/Library/Automator/Combine\ PDF\ Pages.action/Contents/Resources/join.py
ref=references.pdf
doc=Camara_Halac-Application_Materials
rec=../recommendations
help:
	$(CC) -h
	@echo "See the Makefile for more info"

local:
	make cv && open $(PDF) 

all:
	make update
	make cv
	make release
	make references refselect="1 0 2"
	if [[ "$(call)" ]]; then \
		make cover call=$(call); \
		make combine call=$(call); \
	fi

references:
	if [[ ! "$(refselect)" ]]; then \
			$(CC) --references --datadir=$(DATADIR); \
	else \
		echo $(refselect); \
		$(CC) --references --datadir=$(DATADIR) --refselect="$(refselect)"; \
	fi \
	&& open $(DATADIR)/$(ref)

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
	pandoc -i index.html -f html -t docx -o $(OUT)/cv-latest.docx
	sed -ie 's|/Users/fd/Documents/cv/img/profil.jpg|img/profil.jpg|g' index.html
	rm index.htmle 
	cp $(PDF) $(OUT)/cv-latest.pdf

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
		echo "USAGE: make cover call='UniversityModuleFileName'"; \
	else \
		$(CC) --cover=$(call); \
		cd $(DATADIR); \
		pandoc $(PDCFLAGS) -i $(call).tex -f latex -t html -o $(call).html; \
		pandoc -i $(call).html -f html -t docx -o $(call).docx; \
	fi

combine:
	cd $(DATADIR); $(JOIN) --output $(doc)-$(call).pdf \
	$(call).pdf $(TMP).pdf $(ref) $(rec)/*.pdf \
	&& open $(doc)-$(call).pdf; \


.PHONY: cover all new