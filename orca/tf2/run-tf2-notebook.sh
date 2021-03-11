#!/bin/bash
export SPARK_HOME=$SPARK_HOME
export MASTER=local[4]
export ANALYTICS_ZOO_HOME=$ANALYTICS_ZOO_HOME
export ANALYTICS_ZOO_JAR=`find ${ANALYTICS_ZOO_HOME}/lib -type f -name "analytics-zoo*jar-with-dependencies.jar"`
export ANALYTICS_ZOO_PYZIP=`find ${ANALYTICS_ZOO_HOME}/lib -type f -name "analytics-zoo*python-api.zip"`
export ANALYTICS_ZOO_CONF=${ANALYTICS_ZOO_HOME}/conf/spark-analytics-zoo.conf
export PYTHONPATH=${ANALYTICS_ZOO_PYZIP}:$PYTHONPATH

chmod +x ${ZOO_TUTORIALS}/orca/tf2/ipynb2py.sh

set -e


echo "#1 2.1-a-first-look-at-a-neural-network.ipynb"
#timer
start=$(date "+%s")
${ZOO_TUTORIALS}/orca/tf2/ipynb2py.sh ${ZOO_TUTORIALS}/orca/tf2/2.1-a-first-look-at-a-neural-network

cat ${ZOO_TUTORIALS}/orca/tf2/2.1-a-first-look-at-a-neural-network.py > ${ZOO_TUTORIALS}/orca/tf2/tmp_test.py
${SPARK_HOME}/bin/spark-submit \
        --master ${MASTER} \
        --driver-cores 2  \
        --driver-memory 12g  \
        --total-executor-cores 2  \
        --executor-cores 2  \
        --executor-memory 12g \
        --conf spark.akka.frameSize=64 \
        --py-files ${ANALYTICS_ZOO_PYZIP},${ZOO_TUTORIALS}/orca/tf2/tmp_test.py \
        --properties-file ${ANALYTICS_ZOO_CONF} \
        --jars ${ANALYTICS_ZOO_JAR} \
        --conf spark.driver.extraClassPath=${ANALYTICS_ZOO_JAR} \
        --conf spark.executor.extraClassPath=${ANALYTICS_ZOO_JAR} \
        ${ZOO_TUTORIALS}/orca/tf2/tmp_test.py
now=$(date "+%s")
time1=$((now-start))
rm ${ZOO_TUTORIALS}/orca/tf2/tmp_test.py
echo "#1 2.1-a-first-look-at-a-neural-network.ipynb used: $time1 seconds"


echo "#2 6.2-understanding-recurrent-neural-networks"
#timer
start=$(date "+%s")
${ZOO_TUTORIALS}/orca/tf2/ipynb2py.sh ${ZOO_TUTORIALS}/orca/tf2/6.2-understanding-recurrent-neural-networks
sed "s/max_epoch = 10/max_epoch = 2/g" ${ZOO_TUTORIALS}/orca/tf2/6.2-understanding-recurrent-neural-networks.py > ${ZOO_TUTORIALS}/orca/tf2/tmp_test.py
sed -i "s/plt.show()/#/g" ${ZOO_TUTORIALS}/orca/tf2/tmp_test.py    # showing the plot may stuck the test

${SPARK_HOME}/bin/spark-submit \
        --master ${MASTER} \
        --driver-cores 2  \
        --driver-memory 12g  \
        --total-executor-cores 2  \
        --executor-cores 2  \
        --executor-memory 12g \
        --conf spark.akka.frameSize=64 \
        --py-files ${ANALYTICS_ZOO_PYZIP},${ZOO_TUTORIALS}/orca/tf2/tmp_test.py \
        --properties-file ${ANALYTICS_ZOO_CONF} \
        --jars ${ANALYTICS_ZOO_JAR} \
        --conf spark.driver.extraClassPath=${ANALYTICS_ZOO_JAR} \
        --conf spark.executor.extraClassPath=${ANALYTICS_ZOO_JAR} \
        ${ZOO_TUTORIALS}/orca/tf2/tmp_test.py
now=$(date "+%s")
time2=$((now-start))
rm ${ZOO_TUTORIALS}/orca/tf2/tmp_test.py
echo "#2 6.2-understanding-recurrent-neural-networks used: $time2 seconds"

echo "Summary:"
echo "#1 2.1-a-first-look-at-a-neural-network used: $time1 seconds"
echo "#2 6.2-understanding-recurrent-neural-networks used: $time2 seconds"


