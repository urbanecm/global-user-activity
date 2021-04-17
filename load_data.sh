#!/bin/bash

set -e

DATABASE_NAME="s54712__global_user_info"

scriptdir="`dirname \"$0\"`"
cd $scriptdir

mkdir /tmp/$$
echo /tmp/$$

(echo "DROP TABLE undos;"; cat schema/undos.sql) | mysql -h tools-db $DATABASE_NAME

curl -s https://noc.wikimedia.org/conf/dblists/all.dblist | sed 1d > /tmp/$$/all.dblist
curl -s https://noc.wikimedia.org/conf/dblists/private.dblist | sed 1d > /tmp/$$/private.dblist
curl -s https://noc.wikimedia.org/conf/dblists/fishbowl.dblist | sed 1d > /tmp/$$/fishbowl.dblist
curl -s https://noc.wikimedia.org/conf/dblists/closed.dblist | sed 1d > /tmp/$$/closed.dblist
grep -vf /tmp/$$/private.dblist -f /tmp/$$/fishbowl.dblist -f /tmp/$$/closed.dblist /tmp/$$/all.dblist | grep -v -e '^labswiki$' -e '^labtestwiki$' -e '^apiportalwiki$' > /tmp/$$/wikis.dblist

while read db; do
	sql $db < undos-and-rollbacks.sql > /tmp/$$/data.tsv
	echo "LOAD DATA LOCAL INFILE '/tmp/$$/data.tsv' IGNORE INTO TABLE undos IGNORE 1 LINES;" | mysql -h tools-db $DATABASE_NAME
done < /tmp/$$/wikis.dblist

rm -rf /tmp/$$$
