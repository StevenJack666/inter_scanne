#!/bin/sh

echo 'start package'

cd ../../

ls -al


date_time=$(date +%m_%d_%H_%M)
echo $date_time
package_name=${date_time}_vcrawl

tar czvf  ${package_name}.tar.gz  vcrawl

