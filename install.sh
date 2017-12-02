#!/bin/bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

apt-get -y install python-nautilus
apt-get -y install --reinstall python-gi
mkdir -p /usr/share/nautilus-python/extensions/
ln -s $DIR/src/OpenNautilus_extension.py /usr/share/nautilus-python/extensions/OpenNautilus_extension.py
chmod 755 $DIR/src/OpenNautilus_extension.py

bold=$(tput bold)
normal=$(tput sgr0)

echo ""
echo "${bold}Please restart Nautilus using this command without sudo privileges!!${normal}"
echo "nautilus -q; nautilus &"
