FROM python:3.10@sha256:1e5e9ee5b5d12ec9c803eb6166ae4862641d21ed259d0856e34999a1f36b0498

WORKDIR /app

RUN apt update && apt install -y gnupg libpq-dev unixodbc-dev apt-transport-https curl ca-certificates
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
&& curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list >> /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y msodbcsql17

COPY . /app

CMD ["/bin/bash"]

