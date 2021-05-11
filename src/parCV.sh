#!/bin/bash

if [[ $1 ]]
then
	infile=$1
else
	echo "no input filename specified (arg 1)"
	exit 1
fi

if [[ $2 ]]
then
	oufile=$2
else
	echo "no output filename specified (arg 2). Using $infile-par"
	oufile=$infile-par
fi

tn=".feed.entry[].content.\"\$t\""


jq --arg tn "$tn" "$tn" $infile > $oufile.json

