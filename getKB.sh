#!/usr/bin/sh


read -p "Input the path you want to store the HPO2Gene KnowledgeBase [default path: ./lib]: " h2gpath

echo "downloading HPO2Gene KnowledgeBase........"
wget https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/H2GKBs.zip
echo "unzipping H2GKBs.zip........"

if [[ -z "$h2gpath" ]]
then
    h2gpath='./lib'
fi


mkdir -p $h2gpath
echo "$h2gpath" > ./lib/h2gpath.config

unzip -q H2GKBs.zip -d $h2gpath
echo "H2GKB installed in $h2gpath."
rm H2GKBs.zip
