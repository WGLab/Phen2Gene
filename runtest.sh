#!/usr/bin/sh


echo "Running the testing data......"
mkdir -p rankings
python generate_ranking_data.py -f -stat tesitngdata_stat > KB_test_pipeline.log && echo "Finished." && echo "tsv files are in rankings/" && echo "Generating figures......." && sh accuracy.sh
echo "Finished"


