#!/bin/bash
echo "========================================="
echo "Running UI tests"
echo "========================================="
echo "WARNING these tests should not be run on production"
read -p "Are you sure you want to continue [Y/y]: "  cont

if [ $cont = "Y" ]; then
    echo "Running UI tests"
    winpty docker-compose exec mlsb behave;
elif [  $cont = "y" ]; then
    echo "Running UI tests"
    winpty docker-compose exec mlsb behave;
else
    echo "Not running tests, have a nice day"
fi