#!/bin/bash

DIRECTORY="/openssl-gost/"
KEY="keys/letus.pem"


function backup
{
    echo "backup";
}

function sign
{
    $DIRECTORY/bin/openssl smime -sign -in request.xml -out request.xml.sign -signer $KEY -outform DER
}

function info
{
    echo "info";
}

function test
{
    echo "test";
}

function help
{
    echo "Usage: $0 [backup] [sign] [info] [test]";
}


case $1 in 
backup) backup;;
sign) sign;;
info) info;;
test) test;;
*) help;;
esac
