#!/bin/sh
# wait-for-postgres.sh

set -e
echo "print1: ${POSTGRES_DB}"
echo "print2: "
host="$1"
user="$2"
password="$3"
shift 3
cmd="$@"

until PGPASSWORD="$password" psql -h "$host" -U "$user" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

exec $cmd


