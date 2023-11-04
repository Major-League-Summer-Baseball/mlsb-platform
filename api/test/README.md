# mlsb-platform - tests
All test cases should be begin with test*.py

## Running Tests On Docker
Whole test suite: `docker-compose exec mlsb python -m unittest discover -s api/test -p test*.py`
Single test: `docker-compose exec mlsb python -m unittest discover -s api/test -p <TEST_SUITE>.py`

## Running Tests On cmd
Whole test suite: `python -m unittest discover -s api/test -p test*.py`
Single test: `python -m unittest discover -s api/test -p TESTFILE.py`
