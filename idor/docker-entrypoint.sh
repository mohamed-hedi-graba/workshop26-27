#!/bin/sh
set -e

DB_FILE="${INKWELL_DB:-/app/inkwell.db}"

# Seed the database on first run (when no DB file exists yet).
if [ ! -f "$DB_FILE" ]; then
  echo "No database found at $DB_FILE — seeding sample data..."
  mkdir -p "$(dirname "$DB_FILE")"
  python -m app.seed
fi

exec "$@"
