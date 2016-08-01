#!/bin/bash

OPENSSLVERSION=1.0.2h
NOW=`date +'%Y%m%d'`
DIRECTORY=/openssl-gost


echo "Creating backup"
tar -cvjpf $DIRECTORY/backup-$NOW.tar.bz2 $DIRECTORY{/bin,/lib,/ssl,/include}

echo "Downloading last openssl"
wget -c https://www.openssl.org/source/openssl-$OPENSSLVERSION.tar.gz -P $DIRECTORY


echo "Uncompressing openssl"

if ! [ -d $DIRECTORY/src ]; then
    mkdir $DIRECTORY/src
fi


tar -xvzf $DIRECTORY/openssl-$OPENSSLVERSION.tar.gz -C $DIRECTORY/src


echo "Compiling new version of openssl `$OPENSSLVERSION`"

cd $DIRECTORY/src/openssl-$OPENSSLVERSION
./config shared zlib enable-rfc3779 --prefix=$DIRECTORY
make depend
make
make install


echo "Updating openssl.conf for GOST supporting"
sed -i -e '1 s/^/openssl_conf = openssl_def\n/;' $DIRECTORY/ssl/openssl.cnf
sed -i "$ s/^/[openssl_def]\nengines = engine_section\n\n[engine_section]\ngost = gost_section\n\n[gost_section]\nengine_id = gost\ndefault_algorithms = ALL\n\n/;" $DIRECTORY/ssl/openssl.cnf
#sed -i -e "$a s/^/[openssl_def]\nengines = engine_section\n\n[engine_section]\ngost = gost_section\n\n[gost_section]\nengine_id = gost\ndefault_algorithms = ALL\n\n/;" $DIRECTORY/ssl/openssl.cnf
