#!/usr/bin/env bash

tar -pczf packages.tar.gz packages
cat ubuntu_custom_X_install.sh packages.tar.gz > Ubuntu_Openbox_Desktop_Installer.bin
chmod u+x Ubuntu_Openbox_Desktop_Installer.bin
rm -f packages.tar.gz

