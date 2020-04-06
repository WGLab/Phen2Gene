#!/usr/bin/sh

wget https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/testing_data.zip -O testing_data.zip
#mkdir -p testing_data
echo "unzipping the data..........."
unzip -q testing_data.zip 
echo "All data unzipped."
rm testing_data.zip
