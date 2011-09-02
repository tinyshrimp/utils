#!/usr/bin/env bash

SELECTED_PACKAGES=''
TMP_DIR='/tmp/custom-installation'

package_select() {
    SELECTED_PACKAGES=''
    base_packages="$1"

    need_packages=''
    for package in $base_packages
    do
        if [ "`dpkg --list | grep $package`" == "" ]; then
            if [ "${need_packages}" == "" ]; then
                need_packages="${package}"
            else
                need_packages="${need_packages} ${package}"
            fi
        fi
    done

    if [ "${need_packages}" != "" ]; then
        echo 
        echo '--------------------------------------------------------------------'
        echo 'Do you want to install follow packages?'
        echo "Install ${need_packages}"
        echo '--------------------------------------------------------------------'
        echo "y/N/Custom (default is y):"
        while read select
        do
            if [ "${select}" = "" ] || [ "${select}" = "y" ]; then
                SELECTED_PACKAGES="${need_packages}"
                break
            elif [ "${select}" = "Custom" ]; then
                echo 'Please enter the names of packages.'
                echo 'Split them with whitespace.'
                while read packages
                do
                    if [ "${packages}" != "" ]; then
                        echo 'Follow packages will be installed:'
                        echo "${packages}"
                        echo 'Are you sure? (y/N)'
                        while read sure
                        do
                            if [ "${sure}" = "y" ]; then
                                SELECTED_PACKAGES="${packages}"
                                break
                            fi
                        done
                    fi
                    break
                done
                break
            elif [ "${select}" = "n" ] || [ "${select}" = "N" ]; then
                break
            else
                echo "y/N/Custom (default is y):"
                continue
            fi
        done
    fi
}

install_packages() {
    package_select "$1"
    if [ "${SELECTED_PACKAGES}" != "" ]; then
        while true
        do
            sudo apt-get install ${SELECTED_PACKAGES} -y

            RETRY=0
            if [ "$?" != 0 ]; then
                echo 
                echo "*************************************************"
                echo " Failed to download packages."
                echo " Do you want to retry or abandon these packages? "
                echo "*************************************************"
                echo " y to retry and A to abandon (y/A)"
                while read select
                do
                    if [ "${select}" = "" ] || [ "${select}" = "y" ] || "${select}" = "Y" ]; then
                        RETRY=1
                        break
                    elif [ "${select}" = "A" ]; then
                        break
                    else:
                        echo " Please enter you choice"
                        echo " y to retry and A to abandon (y/A)"
                        continue
                    fi
                done
            else
                return 0 # succeed to install
            fi
            
            if [ "${RETRY}" != "1" ]; then
                return 2 # install failed
            fi
        done
        echo
    else
        return 1 # no package need be installed
    fi
}

###############################################################################
# check linux version
###############################################################################
PUBLISH_ID=`lsb_release -is`
CODENAME=`lsb_release -cs`
RELEASE=`lsb_release -rs`

echo
echo '--------------------------------------------------------------------'
echo 'Check system version'
echo '--------------------------------------------------------------------'

if [ "${PUBLISH_ID}" != "Ubuntu" ]; then
    echo 'Invalid publish version.'
    echo 'This custom installation script only could be used for Ubuntu now.'
    exit 1
fi

echo "Publish : ${PUBLISH_ID}"
echo "Codename: ${CODENAME}"
echo "Release : ${RELEASE}"
echo '---------------------------------'
echo 'Done. All OK.'

###############################################################################
# extract packages
###############################################################################

echo
echo '--------------------------------------------------------------------'
echo 'Extract Packages'
echo '--------------------------------------------------------------------'

if [ ! -d "${TMP_DIR}" ]; then
    mkdir -p "${TMP_DIR}"
fi

MSG=`sed -n -e '1,/^exit 0$/!p' $0 > "${TMP_DIR}/packages.tar.gz"`
if [ "$?" != "0" ]; then
    echo 'Failed to extract packages.'
    echo '${MSG}'
    exit 2
fi

cd "${TMP_DIR}"
MSG=`tar -zxvf "${TMP_DIR}/packages.tar.gz" -C "${TMP_DIR}" >/dev/null 2>&1`
if [ "$?" != "0" ]; then
    echo 'Failed to extract packages.'
    echo "${MSG}"
    exit 2
fi

echo 'Done. All OK'

###############################################################################
# replace sources list with mirrors.163.com
###############################################################################

echo
echo '--------------------------------------------------------------------'
echo 'Get sources list from mirrors.163.com'
echo '--------------------------------------------------------------------'

echo 'Do you want use apt source of mirrors.163.com to replace '
echo 'your original sources list? (y/N) [default is y]'
while read select
do
    if [ "${select}" = "" ] || [ "${select}" = "y" ] || [ "${select}" = "Y" ]; then
        # get sources list from mirrors.163.com
        OLD_SOURCE_LIST="/etc/apt/sources.list"
        NEW_SOURCE_LIST="sources.list.${CODENAME}"
        URL="http://mirrors.163.com/.help/${NEW_SOURCE_LIST}"

        wget -c "${URL}"
        if [ "$?" != "0" ]; then
            echo 'Cannot get the new sources.list file from mirrors.163.com.'
            echo 'Default offical sources.list will be used.'
        else
            # replace sources list
            if [ -f "${NEW_SOURCE_LIST}" ]; then
                sudo mv "${OLD_SOURCE_LIST}" "${OLD_SOURCE_LIST}.bak"
                sudo mv "${NEW_SOURCE_LIST}" "${OLD_SOURCE_LIST}"
            fi
        fi
        break
    else
        echo 'User canceled'
        break
    fi
done

##############################################################################
# upgrade system
##############################################################################

echo
echo '--------------------------------------------------------------------'
echo 'Upgrade system'
echo '--------------------------------------------------------------------'

# update
sudo apt-get update

# upgrade
sudo apt-get upgrade -y
if [ "$?" = 0 ]; then
    sudo update-grub
fi

##############################################################################
# install packages
##############################################################################

# install pae kernel
echo
echo '--------------------------------------------------------------------'
echo 'Install pae kernel for 32bit system'
echo 'NOTICE:'
echo '  Please DONT install this kernel if your system is running in '
echo 'a virtual machine. Otherwise, the system will cannot be started.'
echo '--------------------------------------------------------------------'
install_packages 'linux-generic-pae'
if [ "$?" = 0 ]; then
    sudo update-grub
fi

# install desktop
echo
echo '--------------------------------------------------------------------'
echo 'Install X, gdm and Openbox'
echo '--------------------------------------------------------------------'
sudo apt-get install xorg openbox openbox-themes gdm -y

# install base tools
echo
echo '--------------------------------------------------------------------'
echo 'Install Tint2, PCManFM, feh, obconf, lxterminal, lxappearance'
echo '        wicd and xscreensaver'
echo '--------------------------------------------------------------------'
sudo apt-get install tint2 feh pcmanfm obconf lxterminal lxappearance wicd xscreensaver -y

# install language support
echo
echo '--------------------------------------------------------------------'
echo 'Install Language Support Tool'
echo '--------------------------------------------------------------------'
install_packages 'language-selector-gnome'

# install web tools
echo
echo '--------------------------------------------------------------------'
echo 'Install Firefox and Flash plugin'
echo '--------------------------------------------------------------------'
install_packages 'firefox flashplugin-installer'

# install text editor
echo
echo '--------------------------------------------------------------------'
echo 'Install Gvim and LibreOffice'
echo '--------------------------------------------------------------------'
install_packages 'vim-gtk libreoffice'

# install compression tools
echo
echo '--------------------------------------------------------------------'
echo 'Install Compression Tool'
echo '--------------------------------------------------------------------'
install_packages 'file-roller rar unrar p7zip-full'

# install remote desktop tools
echo
echo '--------------------------------------------------------------------'
echo 'Install Remote Desktop Tool'
echo '--------------------------------------------------------------------'
install_packages 'python python-wxgtk2.8 rdesktop'
if [ "`dpkg --list | grep 'rdesktop'`" != "" ]; then
    sudo dpkg -i "${TMP_DIR}/packages/remote-desktop_0.0.1-14_all.deb"
fi

##############################################################################
# copy openbox config for user
##############################################################################
echo
echo '--------------------------------------------------------------------'
echo 'Copying default config files of Openbox to .config/openbox ...'
echo '--------------------------------------------------------------------'

mkdir -p ${HOME}/.config/openbox
cp /etc/xdg/openbox/autostart.sh "${HOME}/.config/openbox/"
cp /etc/xdg/openbox/rc.xml "${HOME}/.config/openbox/"
cp "${TMP_DIR}/packages/wallpaper.jpg" "${HOME}/.config/openbox/"

##############################################################################
# add scripts autostart.sh
##############################################################################
echo
echo '--------------------------------------------------------------------'
echo 'Appending auto start applications to .config/openbox/autostart.sh ...'
echo '--------------------------------------------------------------------'

echo >> "${HOME}/.config/openbox/autostart.sh"

if [ "`dpkg --list | grep 'xscreensaver'`" != "" ]; then
    echo 'xscreensaver -nosplash &' >> "${HOME}/.config/openbox/autostart.sh"
fi

echo 'sleep 5' >> "${HOME}/.config/openbox/autostart.sh"

if [ "`dpkg --list | grep 'tint2'`" != "" ]; then
    echo 'tint2 &' >> "${HOME}/.config/openbox/autostart.sh"
fi

echo 'wicd-client &' >> "${HOME}/.config/openbox/autostart.sh"
echo 'eval `cat ~/.fehbg` &' >> "${HOME}/.config/openbox/autostart.sh"

if [ "`dpkg --list | grep 'feh'`" != "" ]; then
    feh --bg-fill "${HOME}/.config/openbox/wallpaper.jpg"
    echo 'eval `cat ~/.fehbg` &'
fi

echo 'Done'

##############################################################################
# add scripts menu.xml
##############################################################################
echo
echo '--------------------------------------------------------------------'
echo 'Creating menu ...'
echo '--------------------------------------------------------------------'

# add xml header
echo '<?xml version="1.0" encoding="UTF-8"?>' >> "${HOME}/.config/openbox/menu.xml"
echo '<openbox_menu xmlns="http://openbox.org/"' >> "${HOME}/.config/openbox/menu.xml"
echo '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' >> "${HOME}/.config/openbox/menu.xml"
echo '        xsi:schemaLocation="http://openbox.org/' >> "${HOME}/.config/openbox/menu.xml"
echo '                file:///usr/share/openbox/menu.xsd">' >> "${HOME}/.config/openbox/menu.xml"

# add root menu node
echo '<menu id="root-menu" label="Openbox 3">' >> "${HOME}/.config/openbox/menu.xml"

# add shutcuts menu part
echo '  <separator label="Shutcuts" />' >> "${HOME}/.config/openbox/menu.xml"

TERMINAL=''
if [ "`dpkg --list | grep 'lxterminal'`" != "" ]; then
    TERMINAL='lxterminal'
elif [ "`dpkg --list | grep 'xterm'`" != "" ]; then
    TERMINAL='xterm'
fi

if [ "${TERMINAL}" != "" ]; then
    echo '  <item label="Terminal emulator">' >> "${HOME}/.config/openbox/menu.xml"
    echo "    <action name=\"Execute\"><execute>${TERMINAL}</execute></action>" >> "${HOME}/.config/openbox/menu.xml"
    echo '  </item>' >> "${HOME}/.config/openbox/menu.xml"
fi

if [ "`dpkg --list | grep 'firefox'`" != "" ]; then
    echo '  <item label="Web browser">' >> "${HOME}/.config/openbox/menu.xml"
    echo '    <action name="Execute"><execute>firefox</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '  </item>' >> "${HOME}/.config/openbox/menu.xml"
fi

if [ "`dpkg --list | grep 'pcmanfm'`" != "" ]; then
    echo '  <item label="File Browser">' >> "${HOME}/.config/openbox/menu.xml"
    echo '    <action name="Execute"><execute>pcmanfm</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '  </item>' >> "${HOME}/.config/openbox/menu.xml"
fi

if [ "`dpkg --list | grep 'vim-gtk'`" != "" ]; then
    echo '  <item label="Text Editor">' >> "${HOME}/.config/openbox/menu.xml"
    echo '    <action name="Execute"><execute>gvim</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '  </item>' >> "${HOME}/.config/openbox/menu.xml"
fi

    echo '' >> "${HOME}/.config/openbox/menu.xml"

# add applications menu part
echo '  <separator label="Applications" />' >> "${HOME}/.config/openbox/menu.xml"

echo '  <menu id="accessories-menu" label="Accessories">' >> "${HOME}/.config/openbox/menu.xml"
echo '  </menu>' >> "${HOME}/.config/openbox/menu.xml"

if [ "`dpkg --list | grep 'libreoffice'`" != "" ]; then
    echo '  <menu id="office-menu" label="Office">' >> "${HOME}/.config/openbox/menu.xml"

    echo '    <item label="LibreOffice Writer">' >> "${HOME}/.config/openbox/menu.xml"
    echo '      <action name="Execute"><execute>libreoffice -writer</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"
    
    echo '    <item label="LibreOffice Spreesheet">' >> "${HOME}/.config/openbox/menu.xml"
    echo '      <action name="Execute"><execute>libreoffice -calc</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"
    
    echo '    <item label="LibreOffice Presentation">' >> "${HOME}/.config/openbox/menu.xml"
    echo '      <action name="Execute"><execute>libreoffice -impress</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"

    echo '  </menu>' >> "${HOME}/.config/openbox/menu.xml"
fi

echo '  <menu id="config-menu" label="Configuration">' >> "${HOME}/.config/openbox/menu.xml"

if [ "`dpkg --list | grep 'language-selector-gnome'`" != "" ]; then
    echo '    <item label="Language Support">' >> "${HOME}/.config/openbox/menu.xml"
    echo '      <action name="Execute"><execute>gksudo gnome-language-selector</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"
fi
  
if [ "`dpkg --list | grep 'ibus-gtk'`" != "" ]; then
    echo '    <item label="IBus Setup">' >> "${HOME}/.config/openbox/menu.xml"
    echo '        <action name="Execute"><execute>ibus-setup</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"
fi
    
if [ "`dpkg --list | grep 'obconf'`" != "" ]; then
    echo '    <item label="ObConf">' >> "${HOME}/.config/openbox/menu.xml"
    echo '      <action name="Execute"><execute>obconf</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"
fi
  
if [ "`dpkg --list | grep 'lxappearance'`" != "" ]; then
    echo '    <item label="Gtk Themes">' >> "${HOME}/.config/openbox/menu.xml"
    echo '      <action name="Execute"><execute>lxappearance</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
    echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"
fi

echo '    <item label="Reconfigure">' >> "${HOME}/.config/openbox/menu.xml"
echo '      <action name="Reconfigure" />' >> "${HOME}/.config/openbox/menu.xml"
echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"

echo '    <item label="Restart">' >> "${HOME}/.config/openbox/menu.xml"
echo '      <action name="Restart" />' >> "${HOME}/.config/openbox/menu.xml"
echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"

echo '  </menu>' >> "${HOME}/.config/openbox/menu.xml"

echo '  <!-- This requires the presence of the 'menu' package to work -->' >> "${HOME}/.config/openbox/menu.xml"
echo '  <separator label="Workspaces" />' >> "${HOME}/.config/openbox/menu.xml"
echo '  <menu id="client-list-menu" />' >> "${HOME}/.config/openbox/menu.xml"

echo '  <separator label="Logout" />' >> "${HOME}/.config/openbox/menu.xml"
echo '  <menu id="power-menu" label="Power">' >> "${HOME}/.config/openbox/menu.xml"

echo '    <item label="Logout">' >> "${HOME}/.config/openbox/menu.xml"
echo '      <action name="Exit" />' >> "${HOME}/.config/openbox/menu.xml"
echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"

echo '    <!--' >> "${HOME}/.config/openbox/menu.xml"
echo '    To make normal user could run reboot and shutdown command, you need' >> "${HOME}/.config/openbox/menu.xml"
echo '    1. add power group' >> "${HOME}/.config/openbox/menu.xml"
echo '        $ groupadd power' >> "${HOME}/.config/openbox/menu.xml"
echo '    2. add your user to power group' >> "${HOME}/.config/openbox/menu.xml"
echo '        $ sudo visudo -f /etc/sudoers' >> "${HOME}/.config/openbox/menu.xml"
echo '       and then add follow lines to then end of file:' >> "${HOME}/.config/openbox/menu.xml"
echo '        %power ALL=(root) NOPASSWD: /sbin/reboot' >> "${HOME}/.config/openbox/menu.xml"
echo '        %power ALL=(root) NOPASSWD: /sbin/shutdown' >> "${HOME}/.config/openbox/menu.xml"
echo '    -->' >> "${HOME}/.config/openbox/menu.xml"
echo '    <item label="Reboot">' >> "${HOME}/.config/openbox/menu.xml"
echo '      <action name="Execute"><execute>sudo /sbin/reboot</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"

echo '    <item label="Shutdown">' >> "${HOME}/.config/openbox/menu.xml"
echo '      <action name="Execute"><execute>sudo /sbin/shutdown -h now</execute></action>' >> "${HOME}/.config/openbox/menu.xml"
echo '    </item>' >> "${HOME}/.config/openbox/menu.xml"

echo '  </menu>' >> "${HOME}/.config/openbox/menu.xml"

echo '</menu>' >> "${HOME}/.config/openbox/menu.xml"
echo '</openbox_menu>' >> "${HOME}/.config/openbox/menu.xml"

echo 'Done'

##############################################################################
# set default openbox theme here
##############################################################################
echo
echo '--------------------------------------------------------------------'
echo ' Set default theme of Openbox to GoldEx'
echo '--------------------------------------------------------------------'

if [ "`dpkg --list | grep 'obconf'`" != "" ]; then
    if [ -f "${TMP_DIR}/packages/GoldEx.obt" ]; then
        echo
        echo 'Install and apply default openbox theme - GoldEx ...'

        obconf --install "${TMP_DIR}/packages/GoldEx.obt"

        echo 'Done'
    fi
fi

echo 
echo "=========================================="
echo " All packages have been installed."
echo " You could reboot system now."
echo " Please select 'Openbox Session' on login screen."
echo " Thanks for installed this desktop."
echo " Wish you enjoy it."
echo "=========================================="

exit 0
