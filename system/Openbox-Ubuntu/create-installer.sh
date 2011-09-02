#!/usr/bin/env bash

if [ "$1" = "clean" ]; then
    rm -rf dist
    exit $?
else
    tar -pczf packages.tar.gz packages

    if [ ! -d dist ]; then
        mkdir dist
    fi

    cat ubuntu_custom_X_install.sh packages.tar.gz > dist/Ubuntu_Openbox_Desktop_Installer.bin
    chmod u+x dist/Ubuntu_Openbox_Desktop_Installer.bin
    rm -f packages.tar.gz
fi
