# Makefile for cv

all:
	cd src; ./get_cv.py

update:
	cd src; ./get_cv.py --update

index:
	cd .data; pandoc -s --metadata title="CV" -i .temp.tex -f latex -t html -o ../output/index.html

readme:
	cd .data; pandoc -s -i .temp.tex -f latex -t gfm -o ../output/README.md


project:
	rm .data/project.zip
	cd tex; zip ../.data/project.zip *