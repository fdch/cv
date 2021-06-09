#!/bin/bash

while read line; do 
    printf "%s\n    %s\n\n" "def $line(s):" "return tag('$line',s)"
done < commands >> src/latex.py 