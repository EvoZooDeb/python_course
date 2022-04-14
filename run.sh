#!/bin/bash

cat -n Kafer_mittereuropas_oko.txt | sed -rf Kafer_mittereuropas_oko.sed | ./blockgen.py
