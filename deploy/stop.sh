pid=`ps ax | grep -i vcrawl | grep -v grep | awk -e '{print $1}'`

echo $pid

kill -9 $pid
