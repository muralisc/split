#!/bin/sh
# Syntax: 
# backup.sh <what> <how> <where> [whereexactly]
# <what> indicates what you want to backup: mysql, pgsql, riak, data.
# <how> indicates the backup method: ssh, ftp, s3.
# <where> is a <user[:password]@host>.
# [whereexactly] is an optional path on the <where> target, when applicable.
set -e
TAG="$HOSTNAME_$(TZ=UTC date +%Y-%m-%d_%H:%M:%S_UTC)"


case "$1" in
	mysql)
		FILENAME="$TAG.sql.gz"
		FILEPATH="/tmp/$FILENAME"
		mysqldump happydb | gzip > "$FILEPATH"
		;;
	pgsql)
		FILENAME="$TAG.sql.gz"
		FILEPATH="/tmp/$FILENAME"
		pg_dumpall | gzip > "$FILEPATH"
		;;
	riak)
		FILENAME="$TAG.bitcask.tar.gz"
		FILEPATH="/tmp/$FILENAME"
		tar -czf "$FILEPATH" /var/lib/riak
		;;
	data)
		FILENAME="$TAG.data.tar.gz"
		FILEPATH="/tmp/$FILENAME"
		tar -C "$HOME" -czf "$FILEPATH" "data"
		;;
	*)
		echo "Sorry, I don't know how to backup $1."
		exit 1
		;;
esac

SIZE="$(stat --printf %s "$FILEPATH")"
echo "Backup $TAG completed. Its (compressed) size is $SIZE bytes."
