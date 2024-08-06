#!/bin/bash

# Download the file from the given URL
wget https://github.com/gro-david/pydl/raw/main/pydl-linux/dist/pydl -O /tmp/pydl

# Move the downloaded file to /usr/bin
sudo mv /tmp/pydl /usr/bin/pydl

# Make the file executable
sudo chmod +x /usr/bin/pydl

echo "pydl has been installed to /usr/bin/pydl"
