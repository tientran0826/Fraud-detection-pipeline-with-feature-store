FROM minio/minio:latest

RUN mkdir -p /data

ENTRYPOINT ["minio"]
CMD ["server", "/data", "--console-address", ":9001"]
