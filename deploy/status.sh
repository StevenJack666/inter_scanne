#!/bash/bin
pid=`ps ax | grep -i vcrawl | grep -v grep | awk -e '{print $1}'`

echo " runniing id is $pid"
