FROM python:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt-get -y install --no-install-recommends apt-utils git procps gcc unixodbc-dev 2>&1
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN apt autoremove -y && apt clean && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog
RUN python -m pip install pyodbc dbt-core dbt-generator

WORKDIR /workspace/

USER root

CMD ["/bin/bash"]
