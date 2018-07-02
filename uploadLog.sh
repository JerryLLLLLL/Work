#!/bin/bash

HDFS="hadoop dfs "
streaming_dir="/spark/streaming"
$HDFS -rm  "${streaming_dir}"'/tmp/*' > /dev/null 2>&1 
$HDFS -rm  "${streaming_dir}"'/*'     > /dev/null 2>&1 

while [ 1 ]; do
	/home/hadoop/11111/python/loggerCreater.py > /home/hadoop/11111/test.log
	tmplog="access.`date +'%s'`.log"
	$HDFS -put /home/hadoop/11111/test.log ${streaming_dir}/tmp/$tmplog
	$HDFS -mv ${streaming_dir}/tmp/$tmplog ${streaming_dir}
	echo "`date +"%F %T"` put $tmplog to HDFS successed!"
	sleep 1
done 
