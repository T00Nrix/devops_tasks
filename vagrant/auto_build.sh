#!/bin/bash

# check sys arc
OS_TYPE=$(uname)
ARCH=$(uname -m)

if [[ "$OS_TYPE" == "Darwin" && "$ARCH" == "arm64" ]]; then
    echo "VirtualBox does not support on arm64 Mac. Need [MANUAL INSTALL]"
    exit 1
fi

# checker
install_if_needed() {
    local cmd=$1
    local name=$2
    local required_version=$3
    local install_cmd_linux=$4
    local install_cmd_mac=$5

    if ! command -v $cmd &> /dev/null; then
        echo "$name not found. [INSTALLING]"
        if [[ "$OS_TYPE" == "Linux" ]]; then
            eval "$install_cmd_linux"
        elif [[ "$OS_TYPE" == "Darwin" ]]; then
            eval "$install_cmd_mac"
        fi
    else
        version=$($cmd --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        if [[ "$version" != $required_version* ]]; then
            echo "$name VERSION $version installed, but need $required_version.x. [UPDATE]"
            if [[ "$OS_TYPE" == "Linux" ]]; then
                eval "$install_cmd_linux"
            elif [[ "$OS_TYPE" == "Darwin" ]]; then
                eval "$install_cmd_mac"
            fi
        else
            echo "$name [VERSION] $version installed."
        fi
    fi
}

# install virtualBox
install_if_needed "VBoxManage" "VirtualBox" "7.0" \
"sudo apt-get update && sudo apt-get install -y virtualbox" \
"brew install --cask virtualbox"

# install vagrant
install_if_needed "vagrant" "Vagrant" "2.4" \
"sudo apt-get update && sudo apt-get install -y vagrant" \
"brew install vagrant"

# mv to dir
cd "$(dirname "$0")"

# config VAGRANT_CPU && VAGRANT_MEM
export VAGRANT_CPU=${VAGRANT_CPU:-2}
export VAGRANT_MEM=${VAGRANT_MEM:-4096}

# run vagrant up
vagrant up
