#!/bin/bash -e

if [[ $WORDPRESS_DB_HOST == *":"* ]]; then
    HOST=$(echo $WORDPRESS_DB_HOST | cut -d: -f1)
    PORT=$(echo $WORDPRESS_DB_HOST | cut -d: -f2)
else
    HOST=$WORDPRESS_DB_HOST
    PORT=3306
fi

until mysql -h $HOST -P $PORT -D $WORDPRESS_DB_NAME -u $WORDPRESS_DB_USER -p$WORDPRESS_DB_PASSWORD -e '\q' 2>null; do
  sleep 1
done

>&2 echo "Mysql is up - executing command"
