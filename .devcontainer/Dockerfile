FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    sudo \
    libssl-dev \
    libffi-dev \
    python3 \
    fuse \
    procps \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Add keys for ms sql 18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install ms sql 18
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

RUN pip install pyodbc dbt-sqlserver==1.3.0 dbt-core==1.3.0 pytz

WORKDIR /workspace
EXPOSE 8080
CMD ["/usr/local/bin/python", "--version"]
#CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser"]