# mlsb-platform - tests
All test cases should be begin with test*.py

## Running Tests On Docker
Whole test suite: `./run_test.sh`
Single test: `./run_single_test.sh TESTFILE.py`

## Running Tests On cmd
Whole test suite: `python -m unittest discover -s api/test -p test*.py`
Single test: `python -m unittest discover -s api/test -p TESTFILE.py`
