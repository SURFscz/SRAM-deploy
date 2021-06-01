#!/bin/bash

set -e

# this script takes the ca.{crt,key} from the local dir (or generates them if they don't exist) and uses the CA
# to generate and sign keys with CNs specified on the command line

if ! $( openssl version | grep -q OpenSSL )
then
    echo -n "Sorry, you need a real OpenSSL for this.  You have "
    openssl version
    exit 1
fi

if [ $# -lt 1 ]
then
	echo "Please specify machine names CNs"
	exit 1
fi
CNs="$@"

KEYTYPE=RSA:2048
DAYS=36500

if ! [ -e ca.key ]
then
	openssl req \
		-newkey $KEYTYPE -nodes \
		-x509 -days $DAYS \
		-subj '/C=NL/O=SURF/OU=SRAM/CN=SRAM Journalling CA/' \
		-out ca.crt -keyout ca.key
fi

cat >ca.conf <<-EOF
	[ ca ]
	default_ca = this
	[ this ]
	new_certs_dir = .
	certificate = ca.crt
	database = ./index
	private_key = ca.key
	serial = ./serial
	default_days = $DAYS
	default_md = default
	policy = policy_anything
	[ policy_anything ]
	countryName             = optional
	stateOrProvinceName     = optional
	localityName            = optional
	organizationName        = optional
	organizationalUnitName  = optional
	commonName              = supplied
	emailAddress            = optional
EOF

test -e index  || touch index
test -e serial || echo 0001 >serial

for CLIENT in $CNs
do
	if [ -e $CLIENT.key ]
	then
		echo "Refusing to overwrite '$CLIENT.key', skipping $CLIENT"
	else
		openssl req -newkey $KEYTYPE -nodes -utf8 -sha256 -out $CLIENT.csr -keyout $CLIENT.key -subj "/CN=$CLIENT/"
    fi
	if [ -e $CLIENT.crt ]
	then
		echo "Refusing to overwrite '$CLIENT.crt', skipping $CLIENT"
	else
        # note: macos libressl wil always sign with SHA1, even if you requested SHA256
		openssl ca -batch -config ca.conf -notext -in $CLIENT.csr -out $CLIENT.crt
	fi
done

exit 0

