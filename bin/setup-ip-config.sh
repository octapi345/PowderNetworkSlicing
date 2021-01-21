#!/bin/bash

GW=$1

SUDO=/usr/bin/sudo

$SUDO /sbin/iptables -t nat -A POSTROUTING -o `cat /var/emulab/boot/controlif` -j MASQUERADE
$SUDO /sbin/sysctl -w net.ipv4.ip_forward=1
$SUDO /sbin/ip route add 10.233/16 via $GW
