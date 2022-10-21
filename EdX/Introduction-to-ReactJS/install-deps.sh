#!/bin/bash

echo "# Script to install deps to run a static webpage on NPM server"
sudo apt-get install curl
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install nodejs
npm -v
npm install connect serve-static




