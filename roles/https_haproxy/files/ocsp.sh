#!/bin/bash
set -e

maindir=$(pwd)
now=$(date +%s)

# find all certificates, possibly in subdirectories
certs=$(find -name cert.pem)
for cert in $certs
do
    dir=$(dirname $cert)
    cd $maindir/$dir


    # check expiry (but only if the oscp data is more recent than the certificate itself)
    if [ -e "priv+fullchain.pem.ocsp" ] && [ "priv+fullchain.pem.ocsp" -nt "priv+fullchain.pem" ]
    then
        expiry=$( openssl ocsp -respin ./priv+fullchain.pem.ocsp -text -noverify | grep -E '^ +Next Update:' | cut -d: -f2- )
        expiry_sec=$( date --date "$expiry" +%s )
        hourleft=$( echo "($expiry_sec - $now)/3600" | bc )
        if [ $hourleft -gt 24 ]
        then
            echo "OCSP is still valid for $hourleft hours; skipping update"
            continue
        fi
    fi

    # update ocsp data
    OCSP_URL=$(/usr/bin/openssl x509 -noout -ocsp_uri -in cert.pem)
    /usr/bin/openssl ocsp -issuer chain.pem -cert cert.pem -no_nonce -url $OCSP_URL -respout tmp.ocsp

    # only move file in place if update succeeded
    if [ $? -eq 0 ]
    then
        mv tmp.ocsp priv+fullchain.pem.ocsp
        echo "OSCP for $dir updated"
    else
        echo "Couldn't get OSCP response for $dir" >&2
    fi
done
exit 0
