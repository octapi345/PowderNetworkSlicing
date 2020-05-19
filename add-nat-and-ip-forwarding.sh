#!/bin/bash

sudo /sbin/iptables -t NAT -A POSTROUTING -o `cat /var/emulab/boot/controlif` -j MASQUERADE
sudo /sbin/sysctrl -w net.ipv4.ip_forward=1
