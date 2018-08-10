echo "========================================="
echo "  Setting up MLSB with docker!"
echo "========================================="

if [[ -z "${ADMIN}" ]]; then
  ADMIN="admin"
  echo "ADMIN environment variable not set default=admin"
  export ADMIN
fi

if [[ -z "${PASSWORD}" ]]; then
  PASSWORD="password"
  echo "PASSWORD environment variable not set default=password"
  export PASSWORD
fi


if [[ -z "${DATABASE_URL}" ]]; then
  DATABASE_URL="postgresql://$ADMIN:$PASSWORD@postgres:5432/mlsb"
  echo "DATABASE_URL environment variable not set default=postgresql://$ADMIN:$PASSWORD@postgres:5432/mlsb"
  export DATABASE_URL
fi
  
if [[ -z "${KIK}" ]]; then
  KIK="kik"
  echo "KIK environment variable not set default=kik"
  export KIK
fi

if [[ -z "${KIKPW}" ]]; then
  KIKPW="password"
  echo "KIKPW environment variable not set default=password"
  export KIKPW
fi

if [[ -z "${SECRET_KEY}" ]]; then
  SECRET_KEY="secret"
  echo "SECRET_KEY environment variable not set default=secret"
  export SECRET_KEY
fi

if [[ -z "${REDIS_URL}" ]]; then
  REDIS_URL="secret"
  echo "REDIS_URL environment variable not set default=redis://redis:6379/1"
  export REDIS_URL
fi

docker-compose build
echo "Done building"
docker-compose up -d
echo "App is up and runnning"
winpty docker-compose exec mlsb python initDB.py
echo "Database tables created"







