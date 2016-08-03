# 
#
#  Gost algortith support by OPENSSL
#  [Checking, configure, testing]
#
#  MIT License 
#  (c) 2016, Maksim Prokopev
########################################################################################


#!/bin/bash

# for 1.0.* versions only
OPENSSLVERSION=1.0.2h

NOW=`date +'%Y%m%d'`

DIRECTORY=/openssl-gost



SETCOLOR_SUCCESS="echo -en \\033[1;32m"
SETCOLOR_FAILURE="echo -en \\033[1;31m"
SETCOLOR_NORMAL="echo -en \\033[0;39m"



function backup
{
	echo -e "Creating backup"
	if [ -d $DIRECTORY ]; then
		tar -cvjpf $DIRECTORY/backup-$NOW.tar.bz2 $DIRECTORY{/bin,/lib,/ssl,/include}
		$SETCOLOR_SUCCESS
    		echo -n "$(tput hpa $(tput cols))$(tput cub 6)[ok]"
    		$SETCOLOR_NORMAL
    		echo
	else
		$SETCOLOR_FAILURE
		echo -e "--> Directory not found"
    		echo -n "$(tput hpa $(tput cols))$(tput cub 6)[fail]"
    		$SETCOLOR_NORMAL
    		echo
	fi
}


function install
{
	
	if ! [ -d $DIRECTORY]; then
		$SETCOLOR_FAILURE
		echo -e "--> Creating directory $DIRECTORY"
		mkdir $DIRECTORY
		$SETCOLOR_NORMAL
		echo
	fi
	
	$SETCOLOR_SUCCESS
	echo "--> Downloading openssl-$OPENSSLVERSION"
	$SETCOLOR_NORNAL
	echo

	wget -c https://www.openssl.org/source/openssl-$OPENSSLVERSION.tar.gz -P $DIRECTORY

	$SETCOLOR_SUCCESS
	echo "--> Uncompressing openssl"
	$SETCOLOR_NORMAL
	echo

	if ! [ -d $DIRECTORY/src ]; then
		$SETCOLOR_FAILURE
		echo "--> Creating directory $DIRECTORY/src"
    		mkdir $DIRECTORY/src
		$SETCOLOR_NORMAL
		echo
	fi


	#tar -xvzf $DIRECTORY/openssl-$OPENSSLVERSION.tar.gz -C $DIRECTORY/src


	echo "Compiling new version of openssl `$OPENSSLVERSION`"

	cd $DIRECTORY/src/openssl-$OPENSSLVERSION
	./config shared zlib enable-rfc3779 --prefix=$DIRECTORY
	make depend
	make
	make install
}

function update_conf
{
	echo "Updating openssl.conf for GOST supporting"
	sed -i -e '1 s/^/openssl_conf = openssl_def\n/;' $DIRECTORY/ssl/openssl.cnf
	sed -i "$ s/^/[openssl_def]\nengines = engine_section\n\n[engine_section]\ngost = gost_section\n\n[gost_section]\nengine_id = gost\ndefault_algorithms = ALL\n\n/;" $DIRECTORY/ssl/openssl.cnf
#sed -i -e "$a s/^/[openssl_def]\nengines = engine_section\n\n[engine_section]\ngost = gost_section\n\n[gost_section]\nengine_id = gost\ndefault_algorithms = ALL\n\n/;" $DIRECTORY/ssl/openssl.cnf
}

function remove
{
	$SETCOLOR_FAILURE
	echo "--> Removing $DIRECTORY"
	rm -r -f $DIRECTORY;
	$SETCOLOR_NORMAL;
	echo;
}



case $1 in 
backup) backup;;
install) install;;
remove) remove;;
update_conf) update_conf;;
esac

