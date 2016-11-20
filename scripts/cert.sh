#!/bin/bash

DIRECTORY='/openssl-gost'
KEYS='~/keys'


function checkopenssl
{
    if [ -d $DIRECTORY ]
    then return 1
    else return 0
    fi
}

function checkkeys
{
    if [ -d $KEYS ]
    then return 1
    else return 0
    fi
}


function convertPcs12ToPem
{
    $DIRECTORY/bin/openssl pkcs12 –in $KEYS/cert.p12 –out $KEYS/cert.pem
}

function dates
{
    $DIRECTORY/bin/openssl x509 -noout -in $KEYS/certificate.pem -dates
}

function verify
{
    $DIRECTORY/openssl x509 -in $KEYS/certfile.pem -text –noout
}


function list
{
    if [ checkkeys == 1 ]
    then ls -la $KEYS
    else echo "Directory with keys is not exist: $KEYS"
    fi
}


function help
{
    echo "Usage: $0 [convert] [dates] [verify]"
}


case $1 in 
convert) convertPcs12ToPem;;
dates)   dates;;
verify)  verify;;
list)    list;;
*)       help;;
esac
