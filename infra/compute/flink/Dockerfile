FROM flink:1.17.1-scala_2.12

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --no-cache-dir \
    apache-flink==1.17.1 \
    feast \
    redis \
    kafka-python \
    "pandas<2.1.0"

WORKDIR /opt/flink/usrlib

COPY infra/compute/flink/flink_job.py /opt/flink/usrlib/flink_job.py
COPY infra/compute/flink/flink-sql-connector-kafka-3.1.0-1.18.jar /opt/flink/usrlib/flink-sql-connector-kafka-3.1.0-1.18.jar