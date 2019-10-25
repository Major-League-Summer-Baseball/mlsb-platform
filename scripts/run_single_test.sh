#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Need test file name e.g. testSchedule.py"
    echo "./run_single_test.sh TEST_FILE.py"
    exit
fi

echo "========================================="
echo "Running a specific unittest"
echo "========================================="
echo "WARNING these tests should not be run on production"
read -p "Are you sure you want to continue [Y/y]: "  cont
if [ $cont = "Y" ]; then
    echo "Running test: $1"
    winpty docker-compose exec mlsb python -m unittest discover -s api/test -p $1
elif [  $cont = "y" ]; then
    echo "Running test: $1"
    winpty docker-compose exec mlsb python -m unittest discover -s api/test -p $1*.py
else
    echo "Not running tests, have a nice day"
fi