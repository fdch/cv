#!/bin/bash
mc=0
content="\"\$t\""
for file in $1/*
do
	# echo ".feed.entry[$cnt] | .[] | .[]"
	# jq '.feed.entry[] | keys_unsorted' $file
	# echo $mc $file
	jq --arg cnt $mc --arg cn $content ".feed.entry[$cnt].content[$cn]" "$file" |
	

	sed '/"text"/d;s/"/ /g' > $file-parsed.tex 

	if [[ $mc -eq 0 ]]
	then
		cat $file-parsed.tex | 
		sed -e $'s/,/\\\n/g' |
		sed 's/$/}/' |
		sed -e $'s/: /{ /g' | 
		sed '/term/d' |
		sed -e $'s/type/\\\\title/g' |
		sed -e $'s/institution/\\\n\\\\end{position}\\\n\\\\employer/g' |
		sed -e $'s/year/\\\\dates/g' |
		sed -e $'s/department/\\\\location/g' |
		sed -e $'s/class/\\\\begin{position}\\\n/g' > $file-parsed.tex 
	fi
	if [[ $mc -eq 1 ]]
	then
		cat $file-parsed.tex | 
		sed -e $'s/title/\\\\title/g' |
		sed -e $'s/who:/\\\\employer:/g' |
		sed -e $'s/duration/\\\\dates/g' |
		sed -e $'s/where/\\\\location/g' |
		sed -e $'s/description/\\\\begin{position}\\\n/g' |
		sed -e $'s/url/\\\n\\\\end{position}\\\n/g' | 
		sed -e $'s/,/\\\n/g' |
		sed '/type/d' |
		sed 's/$/}/' |
		sed -e $'s/: /{ /g' |
		sed -e $'s/}}/}/g' |
		sed '/{ http/d' > $file-parsed.tex
	fi
	if [[ $mc -eq 2 ]]
	then
		cat $file-parsed.tex | 
		sed -e $'s/category/\\\\title/g' |
		sed -e $'s/who:/\\\\employer:/g' |
		sed -e $'s/year/\\\\dates/g' |
		sed -e $'s/where/\\\n\\\\end{position}\\\n\\\\location/g' |
		sed -e $'s/description/\\\\begin{position}\\\n/g' |
		sed -e $'s/,/\\\n/g' |
		sed 's/$/}/' |
		sed -e $'s/: /{ /g' |
		sed -e $'s/}}/}/g' > $file-parsed.tex
	fi
	if [[ $mc -eq 3 ]]
	then
		cat $file-parsed.tex | 
		sed -e $'s/what/\\\\title/g' |
		sed -e $'s/instrument/\\\\employer/g' |
		sed -e $'s/when/\\\\dates/g' |
		sed -e $'s/where/\\\n\\\\end{position}\\\n\\\\location/g' |
		sed -e $'s/how/\\\\begin{position}\\\n/g' |
		sed -e $'s/,/\\\n/g' |
		sed 's/$/}/' |
		sed -e $'s/: /{ /g' |
		sed -e $'s/}}/}/g' > $file-parsed.tex
	fi

	# sed -e $'s/institution/employer/g' > $file-parsed
	# tail -n +17 < tmp > $file-parsed
	# rm tmp
	((mc=$mc+1))
done

exit 0
cd cv
pdflatex cv_2.tex 
open cv_2.pdf
cd ..
exit 0