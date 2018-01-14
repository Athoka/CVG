#!/bin/bash
python menu.py
/usr/local/spark/bin/spark-submit patrons.py data.txt
cat grade.txt/* > result.txt
python grades.py result.txt