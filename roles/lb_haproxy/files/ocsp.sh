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
        hourleft=$(( ($expiry_sec - $now)/3600 ))
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
        if ! [ -e "priv+fullchain.pem.ocsp" ] || ! diff -q "tmp.ocsp" "priv+fullchain.pem.ocsp" > /dev/null
        then
            echo "OSCP for $dir updated"
            mv tmp.ocsp priv+fullchain.pem.ocsp
            /bin/systemctl reload haproxy.service
        else
            echo "OSCP for $dir unchanged"
            rm tmp.ocsp
        fi
    else
        echo "Couldn't get OSCP response for $dir" >&2
        rm -f tmp.ocsp
    fi
done
exit 0
