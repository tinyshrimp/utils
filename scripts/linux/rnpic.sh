#!/bin/bash

#set -x

FILE_TYPES=( "jpg" "png" "gif" )
PWD=`pwd`

ls | while read line
do 
	isPic=0
	ext=''

	for type in ${FILE_TYPES[@]}
	do
		PATTERN=".*\\.${type}$"
        filename=`echo ${line} | tr '[A-Z]' '[a-z]'`
		cnt=`expr match "${filename}" $PATTERN`
		if [ "${cnt}" != "0" ]
		then
			isPic=1
			ext=${type}
			break
		fi
	done

	if [ ${isPic} -ne 0 ]
	then
		fullpath=${PWD}/${line}
		output=`md5sum "${fullpath}"`
		md5=`expr substr "${output}" 1 32`

		newname=${PWD}/${md5}.${ext}

		if [ "${newname}" != "${fullpath}" ]
		then
			#if [ -f "${newname}" ]
			#then
			#	echo 'Target file existed.'
			#	echo "Source: ${fullpath}"
			#	echo "Target: ${newname}"
			#	eog "${fullpath}" "${newname}" >/dev/null 2>&1
			#
			#	echo -n "Do you want to replace it? [Y/n]:"
			#	read -n 1 replace
			#	if [[ "${replace}" = "Y" ]] || [[ "${replace}" = "y" ]]
			#	then
			#		mv -f "${fullpath}" "${newname}" >/dev/null 2>&1
			#		if [ $? -ne 0 ]
			#		then
			#			echo "Failed to replace target file."
			#		fi
			#	fi
			#else
			#	err=`mv "${fullpath}" "${newname}" 2>&1`
			#	if [ $? -ne 0 ]
			#	then
			#		echo "Failed to rename '${fullpath}' to '${newname}'."
			#		echo "${err}"
			#	fi
			#fi

			err=`mv "${fullpath}" "${newname}" 2>&1`
			if [ $? -ne 0 ]
			then
				echo "Failed to rename '${fullpath}' to '${newname}'."
				echo "${err}"
			fi
		fi
	fi
done
