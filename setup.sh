sudo apt-get update
sudo apt-get install -y \
  build-essential checkinstall \
  postgresql postgresql-contrib postgresql-server-dev-9.3 \
  libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
  python python-pip python-dev

sudo -u postgres createdb mlsb_db
sudo -u postgres psql -c "CREATE USER mlsb_user WITH PASSWORD 'mlsbthebigs';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE \"mlsb_db\" to mlsb_user;"

cd /vagrant
sudo pip install -r requirements.txt

CRED="/vagrant/api/credentials.py"
echo "URL = 'postgresql://mlsb_user:mlsbthebigs@localhost:5432/mlsb_db'" > $CRED
echo "import os; SECRET_KEY = os.urandom(24)" >> $CRED
echo "ADMIN = 'mlsb_user'" >> $CRED
echo "PASSWORD = 'mlsbthebigs'" >> $CRED
echo "KIK = '<idk!!>'" >> $CRED
echo "KIKPW = '<IDK>'" >> $CRED

python initDB.py

echo "========================================="
echo "  Done setting up the MLSB Vagrant box!"
echo "========================================="
