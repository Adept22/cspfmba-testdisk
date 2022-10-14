#!/bin/sh
set -e

# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1" ]; then
	set -- python3 "$@"
fi

if [ "$1" = 'python3' ]; then
	echo "Its python3"

	if [[ ! -z "$DATABASE_URL" ]]; then
		echo "Database URL exist"

		if ls -A db/migrations/migration/versions/*.py > /dev/null 2>&1; then
			echo "Make migrations"

            cd db/migrations
			alembic upgrade head
            cd ../..
		fi
	fi
fi

exec "$@"
