#!/usr/bin/sh
set -x

read -p "Input path for where you want to store the HPO2Gene KnowledgeBase [default path: ./lib]: " h2gpath

read -p "Input path to store scripts for execution [default path: this folder]: " softpath

echo "downloading HPO2Gene KnowledgeBase........"
wget https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/H2GKBs.zip
echo "unzipping H2GKBs.zip........"

if [[ -z "$h2gpath" ]]
then
    h2gpath='lib'
fi

getpath() {
  (
  cd "$(dirname $1)"         # or  cd "${1%/*}"
  echo "$PWD/$(basename $1)" # or  echo "$PWD/${1##*/}"
  )
}

h2gpath=$(getpath $h2gpath)
export h2gpath

mkdir -p $h2gpath
echo "$h2gpath" > ./lib/h2gpath.config

if [[ ! -z "$softpath" ]]
then
    softpath=$(getpath $softpath)
    export softpath
    mkdir -p $softpath
    cp -a phen2gene.py $softpath
    cp -ar lib $softpath
    chmod +x $softpath/phen2gene.py
    chmod +x $softpath/lib/*
    echo "$h2gpath" > $softpath/lib/h2gpath.config
fi

unzip -q H2GKBs.zip -d $h2gpath
echo "H2GKB installed in $h2gpath."
rm H2GKBs.zip
