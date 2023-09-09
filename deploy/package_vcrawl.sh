#!/bin/sh

echo 'start package'

cd ../../

ls -al


date_time=$(date +%Y%m%d%H%M%S)
echo $date_time
package_name=vcrawl${date_time}

tar czvf  ${package_name}.tar.gz  vcrawl

