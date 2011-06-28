#!/usr/bin/env bash

PREFIXES=( '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' '0' 'a' 'b' 'c' 'd' 'e' 'f' )

for prefix in "${PREFIXES[@]}"
do
	if [ ! -d "${prefix}" ]
	then
		mkdir "${prefix}"
	fi
	
	ls | grep "^${prefix}.*" | while read line
	do
		if [ -d "${line}" ]
		then
			continue
		fi
		mv "${line}" "./${prefix}"
	done
done
