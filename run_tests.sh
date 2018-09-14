#!/bin/bash
echo "========================================="
echo "Running unittests"
echo "========================================="
echo "WARNING these tests should not be run on production"
read -p "Are you sure you want to continue [Y/y]: "  cont

if [ $cont = "Y" ]; then
    echo "Running tests"
    winpty docker-compose exec mlsb python -m unittest discover
elif [  $cont = "y" ]; then
    echo "Running tests"
    winpty docker-compose exec mlsb python -m unittest discover
else
    echo "Not running tests, have a nice day"
fi

