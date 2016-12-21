#!/bin/bash
echo -n "Applying blacklist to IPSET..."
ipset -N dropip iphash
xfile=$(cat ip.txt)
for ipaddr in $xfile
do
ipset -A dropip $ipaddr
done
echo "...Done"
echo -n "Applying blacklist to Netfilter..."
iptables -v -I INPUT -m set --match-set dropip src -j DROP
iptables -v -I INPUT -m set --match-set dropip src -j LOG --log-prefix "DROP blacklist entry"
echo "...Done"

