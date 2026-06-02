FROM flink:1.17.1-scala_2.12

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --no-cache-dir \
    apache-flink==1.17.1 \
    feast \
    redis \
    "pandas<2.1.0"

WORKDIR /opt/flink/usrlib