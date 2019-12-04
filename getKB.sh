#!/usr/bin/sh

wget https://github.com/WGLab/Phen2Gene/releases/download/1.0.0/H2GKBs.zip
echo "unzipping H2GKBs.zip........"
unzip -q H2GKBs.zip -d ./lib/ 
echo "H2GKB installed."
rm H2GKBs.zip



