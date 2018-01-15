#!/bin/bash
python menu.py
/usr/local/spark/bin/spark-submit patrons.py data.txt
cat result.txt/* > output.txt
python avgs.py output.txt