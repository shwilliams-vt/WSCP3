# WSCP3

## Overview

This project explores silent data corruption in Apache Spark. I designed a SDC simulator (a fault injector) for Apache Spark and then tested it with a PageRank PySpark application by testing different iteration counts and probabilities of SDC occuring, and analyzed the correctness. For detailed information, see the included report. 

## Replication/Usage of source files

To replicate the experiment or understand how I performed the experiment, follow these steps while inside this directory (performed in Ubuntu 22.04.1). 

0. Install Apache Spark 3.3.0 and Hadoop 3.3.4 HDFS, set up to run in a cluster (add commands to PATH)
1. Copy the example PageRank PySpark operation included in the Apache Spark sample directory to the current working directory.
2. Modify this file by adding:
    a. 3 nested for-loops testing:
        i.   The number of PageRank iterations
        ii.  The probabilities of SDC (0.001, 0.01, 0.1)
        iii. 50 trials
    b. Add a probability parameter to '''computeContribs'''
    c. Wrap the expression '''rank / urls''' with a call to SIMULATE_SDC, and add the probability as the second parameter.
    d. When done, it should resemble '''pageranktest.py'''
3. Call '''~/build_pyspark_fault_injector.sh -i ./pagerank.py -o pagerank_sdc.py''', where '''pagerank.py''' is the modified PageRank application and '''pagerank_sdc.py''' will be the output PySpark app with the library SDC code added.
4. Add '''testpagerank.txt''' to HDFS (e.g. to '''/data/testpagerank.txt''', as it is the PageRank example instance found in the report.
5. Call '''spark-submit --master local[4] pagerank_sdc.py /data/testpagerank.txt >> pagerank_output.txt'''. This will probably take a while
6. Parse the output to find the average relative errors and average deviations by calling '''python3 ./parseresults.py pagerank_output.txt'''. The results will be printed to stdout.

Let me know if you have any questions by emailing me at shwilliams@vt.edu
