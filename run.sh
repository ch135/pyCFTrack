#!/bin/bash

export pyCFTrackers=$PWD

cd lib/eco/features/
python setup.py build_ext --inplace
cd ../../..

cd lib/pysot/utils/
python setup.py build_ext --inplace
cd ../../..

export PYTHONPATH=$PWD:$PYTHONPATH
cd /root/simple_hao/github/pyCFTrackers/examples
python cf_demo.py
<<COMMENT
cd /root/simple_hao/github/pyCFTrackers/eval

python get_vot2016_result.py
python get_vot2018_result.py
python ope_otb.py
python eval_VOT2016.py
python  eval_VOT2018.py
python eval_OTB.py
COMMENT