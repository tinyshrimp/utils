#!/usr/bin/env bash

#set -x

MODE=0
CLEAN=1
BUILD=2
REBUILD=3

if [[ "$1" == "clean" ]]
then
	MODE=${CLEAN}
elif [[ "$1" == "build" ]]
then
	MODE=${BUILD}
elif [[ "$1" == "rebuild" ]]
then
	MODE=${REBUILD}
else
	echo "Unknown argument: $1"
	echo "Usage:"
	echo "  ./build.sh build"
	echo "  ./build.sh clean"
	exit 1
fi

if [ ${MODE} -ne ${BUILD} ]
then
	python setup.py clean --all

	if [ -d 'build' ]
	then
		rm -rf build
	fi

	if [ -d 'dist' ]
	then
		rm -rf dist
	fi

	if [ -d 'remote_desktop.egg-info' ]
	then
		rm -rf remote_desktop.egg-info
	fi
fi

if [ ${MODE} -ne ${CLEAN} ]
then
	python setup.py bdist --formats=gztar,zip

	# build RPM package
	release_number=`cat release_num`
	python setup.py bdist_rpm --post-install rpm_spec.post_install --release ${release_number}

	# create DEB package
	cd dist
	rpm_pkg_name=`ls | grep "remote-desktop-[0-9.-].*\.noarch\.rpm"`
	if [[ "${rpm_pkg_name}" != "" ]]; then
		fakeroot alien -d -c "${rpm_pkg_name}"
	fi
	cd ..

	# increase release number
	release_number=`expr ${release_number} + 1`
	echo ${release_number} > release_num
fi
