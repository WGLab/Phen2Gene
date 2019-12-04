#!/usr/bin/sh


echo "Running the testing data..... It takes 6 minutes......"
python KB_test_pipeline.py -f -stat tesitngdata_stat > KB_test_pipeline.log &
sleep 6m
echo "Finished."
echo "tsv files are in rankings/"
echo "Generating figures......."
sh accuracy.sh
echo "Finished"


