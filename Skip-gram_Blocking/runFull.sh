#!/bin/sh
python3 buildWordsTable.py
python3 generateEmbeddings.py
python3 makePredictions.py
python3 knnModel.py
