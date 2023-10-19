#!bin/bash



task_id=$1
type=$2

JAR_NAME=vcrawl

FULE_NAME=/home/py/package/backend/$JAR_NAME
echo $FULE_NAME

CONFIG_FILE_NAME=application.yml
CONFIG_FILE=/home/ap/scanner/backend/$CONFIG_FILE_NAME

pid=`ps ax | grep -i vcrawl |  grep java | grep -v grep | awk '{print $1}'`
#pid=`ps ax | grep -i ${FULE_NAME} |  grep java | grep -v grep | awk '{print $1}'`
#pid= `ps ax | grep -i ${FULE_NAME} |  grep java | grep -v grep | awk '{print $1}'`

if [ "$pid" ]; then
	echo "error , $JAR_NAME running"
	exit -1;
fi

echo "will start $FULE_NAME"

if (( $type == 1 )); then
  echo "tg run"
  nohup python3.7 ../vcrawl.py  tg --task_id=${task_id} --action=get_message >/home/py/logs/py_tg.log  2>&1 &
elif (( $type==2 )); then
  echo "chagnan run"
  nohup python3.7 ../vcrawl.py crawl --task_id=${task_id} --conf=../changan.conf > /home/py/logs/py_changan.log 2>&1 &
elif (( $type==3 )); then
  echo "darnnet run"
  nohup python3.7 ../vcrawl.py crawl --task_id=${task_id} --conf=../darknet.conf > /home/py/logs/py_darknet.log 2>&1 &
else
  echo "error"
fi
