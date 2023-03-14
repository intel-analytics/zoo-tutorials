# tpch-pyspark

TPC-H queries implemented in PySpark.

### Generating tables

Move to `../tpch-spark/dbgen/`, Under the dbgen directory do:
```
make
```

This should generate an executable called `dbgen`
```
./dbgen -h
```

gives you the various options for generating the tables. The simplest case is running:
```
./dbgen
```
which generates tables with extension `.tbl` with scale 1 (default) for a total of rougly 1GB size across all tables. For different size tables you can use the `-s` option:
```
./dbgen -s 10
```
will generate roughly 10GB of input data.

You can then either upload your data to hdfs or read them locally.

### Running

First compile using:

```
zip -r tpch.zip ./tpch
```

for example, you can run it by:
```
/usr/lib/jvm/java-8-openjdk-amd64/bin/java \
                -XX:-UseCompressedOops \
                -XX:ActiveProcessorCount=4 \
                -Divy.home="/tmp/.ivy" \
                -Dos.name="Linux" \
                -Djdk.lang.Process.launchMechanism=vfork \
                -cp "$SPARK_HOME/conf/:$SPARK_HOME/jars/*" \
                -Xmx5g org.apache.spark.deploy.SparkSubmit \
                --conf spark.sql.shuffle.partitions=8 \
                --py-files ./tpch-pyspark/tpch.zip \
                ./tpch-pyspark/main.py \
                $INPUT_DIR $OUTPUT_DIR true [QUERY]
```

INPUT_DIR is the tpch's data dir.
OUTPUT_DIR is the dir to write the query result.
true is to choose using sql or python function.
The optional parameter [QUERY] is the number of the query to run e.g 1, 2, ..., 22.

--------------
This project is based on [rapoth/spark2's benchmark python](https://github.com/rapoth/spark-2/tree/master/benchmark).
