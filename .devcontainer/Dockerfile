FROM python:3.10-bullseye

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install --no-install-recommends apt-utils git procps gcc 2>&1
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN apt-get install -y unixodbc-dev
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN apt autoremove -y && apt clean && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

RUN python -m pip install pyodbc
RUN python -m pip install -U --pre dbt-sqlserver dbt-generator

WORKDIR /workspace/

USER root

CMD ["/bin/bash"]
