FROM python:3.9 AS p3.9
WORKDIR /app
RUN apt update && apt install -y gnupg libpq-dev unixodbc-dev apt-transport-https curl ca-certificates
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
&& curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list >> /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y msodbcsql17
COPY . /app
CMD ["/bin/bash"]

FROM python:3.10 AS p3.10
WORKDIR /app
RUN apt update && apt install -y gnupg libpq-dev unixodbc-dev apt-transport-https curl ca-certificates
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
&& curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list >> /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y msodbcsql17
COPY . /app
CMD ["/bin/bash"]

FROM python:3.11 AS p3.11
WORKDIR /app
RUN apt update && apt install -y gnupg libpq-dev unixodbc-dev apt-transport-https curl ca-certificates
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
&& curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list >> /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y msodbcsql17
COPY . /app
CMD ["/bin/bash"]

FROM python:3.12 AS p3.12
WORKDIR /app
RUN apt update && apt install -y gnupg libpq-dev unixodbc-dev apt-transport-https curl ca-certificates
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
&& curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list >> /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y msodbcsql17
COPY . /app
CMD ["/bin/bash"]

