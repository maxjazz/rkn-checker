#!/bin/bash

$DIRECTORY=/openssl-gost
$KEYS=/openssl-gost/keys

function convertPcs12ToPem
{
    $DIRECTORY/bin/openssl pkcs12 –in $KEYS/cert.p12 –out $KEYS/cert.pem
}

function dates
{
    $DIRECTORY/bin/openssl x509 -noout -in $KEYS/certificate.pem -dates
}

function verufy
{
    $DIRECTORY/openssl x509 -in $KEYS/certfile.pem -text –noout
}


case $1 in 
convert) convertPcs12ToPem
dates) dates;;
verify) verify;;
esac
