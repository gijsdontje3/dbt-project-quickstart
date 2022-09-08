FROM python:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt-get -y install --no-install-recommends apt-utils 2>&1
RUN apt install -y git procps gcc
RUN apt autoremove -y && apt clean && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

RUN python -m pip install pyodbc dbt-core dbt-generator

WORKDIR /workspace/

USER root

CMD ["/bin/bash"]
