#!/bin/bash
/openssl-gost/bin/openssl smime -sign -in ./request.xml -out ./request.xml.sign -signer keys/letus.pem -outform DER