if [ $# -eq 0 ]
  then
    echo "No arguments supplied, will be installed in current directory"
    DIR=.
else
    DIR=$1
fi
printf "Downloading testing data....\n"
wget -q https://github.com/WGLab/Phen2Gene/releases/download/1.1.0/testing_data.zip
unzip -q testing_data.zip -d $DIR
rm testing_data.zip
printf "Testing data downloaded...\n"
