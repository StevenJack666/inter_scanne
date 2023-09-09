#!/bin/sh

echo 'start run'

net_conf=$1
echo $net_conf

app_conf=application.conf
cd ..


python3 vcrawl.py crawl --conf=$net_conf $app_conf= 2>&1 &