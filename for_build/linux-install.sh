#!/bin/bash

# copy the file
cp ./linux-build/pydl /usr/local/bin/
cp ./pydl-default.conf /usr/local/bin/pydl.conf
# change the directory
cd /usr/local/bin/

# allow the app to run
chmod +x ./pydl

# create an empty config file so we dont get an error
touch pydl.conf

# generate the initial config so the ux is better
pydl generate-config
