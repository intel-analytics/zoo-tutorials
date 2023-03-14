

import sys
import time

from tpch.tpch_function import *
from tpch.tpch_sql import *
from pyspark.sql import SparkSession


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("\t<spark-submit> --master local main.py")
        print("\t\t<tpch_data_root_path> <query_number> <num_iterations> <true for SQL | false for functional>")
        exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    use_sql = sys.argv[3].lower() == "true"
    query_list = []
    if (len(sys.argv) > 4):
        query_number = str(sys.argv[3])
        query_list.append(query_number)
    else:
        query_list = range(1, 23)

    spark = SparkSession.builder.getOrCreate()
    print("Will run " + str(query_list))
    start1 = time.time()
    if (use_sql == False):
        queries = TpchFunctionalQueries(spark, input_dir)
        print("TPCH using python function")
    else:
        queries = TpchSqlQueries(spark, input_dir)
        print("TPCH using SQL directly")
    #action
    queries.part.first()
    for iter in query_list:
        query_number = iter
        print("TPCH Starting query #{0}".format(iter))
        start = time.time()
        out = getattr(queries, "q" + str(query_number))()
        out.write.mode("overwrite").format("csv").option("header", "true").save(output_dir + "./Q" + str(query_number))
        end = time.time()
        print("query%s --finished--,time is %s s" % (query_number, end - start))
    end1 = time.time()
    print("total time is %f s" % (end1 - start1))

    spark.stop()


if __name__ == '__main__':
    main()