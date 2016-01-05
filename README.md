# mlsb-platform
A platform for mlsb


## Development

0. `pip install -r requirements.txt`
1. Have PostgreSQL installed on your machine
2. Add a file `api/credentials.py` that exposes the following variables:
  - `URL` (something like `postgresql://username@localhost:5432/mlsb_db`)
  - `SECRET_KEY` (some random data. e.g. `import os; os.urandom(24)`)
  - `ADMIN` (arbitrary user name, to be used as admin login)
  - `PASSWORD` (arbitrary password, for admin login)
3. From the root of the project run `python testData.py` to initialize the DB