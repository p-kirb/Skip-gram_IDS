#!/bin/sh
cd ../../
mkdir CTU-43_bidirectional-sample
cd CTU-43_bidirectional-sample
curl https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-43/detailed-bidirectional-flow-labels/capture20110811.binetflow -o "capture20110811.binetflow"
cd ../SCC300HoneypotProject/ML_Blocking
python3 knnModel.py