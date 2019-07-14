#!/bin/bash
OCSP_URL=$(/usr/bin/openssl x509 -noout -ocsp_uri -in cert.pem)
OCSP_HOST=$(echo $OCSP_URL | cut -d/ -f3)
/usr/bin/openssl ocsp -issuer chain.pem -cert cert.pem -url $OCSP_URL -header Host=$OCSP_HOST -respout priv+fullchain.pem.ocsp
