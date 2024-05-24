FROM python:3.8.16-slim-bullseye as python

# Python build stage
FROM --platform=linux/amd64 python

ARG BUILD_ENVIRONMENT=production


RUN apt-get update\
    && apt-get -y upgrade


# Install apt packages
RUN apt-get install --no-install-recommends -y \
    libncurses5-dev libgdbm-dev libnss3-dev \
    libssl-dev libreadline-dev libffi-dev libxml2-dev libxslt1-dev libevent-dev \
    libsasl2-dev libldap2-dev pkg-config libtiff5-dev libjpeg62-turbo-dev libjpeg-dev \
    zlib1g-dev libfreetype6-dev liblcms2-dev liblcms2-utils libwebp-dev tcl8.6-dev \
    tk8.6-dev libyaml-dev fontconfig xfonts-75dpi xfonts-base xfonts-encodings xfonts-utils \
    # dependencies for building Python packages
    build-essential sudo libxslt-dev libzip-dev libldap2-dev libsasl2-dev python3-setuptools node-less pkg-config \
    # psycopg2 dependencies
    libpq-dev libxmlsec1 libxmlsec1-dev  \
    # Added libssl for SSL support on librdkafka's build. This is necessary for macOS build. \
    libssl-dev \
    wget \
    git \
    gnupg2 \
    software-properties-common


# Clone Odoo repository
RUN git clone https://www.github.com/odoo/odoo.git --depth 1 \
    --branch 13.0 --single-branch /opt/odoo/odoo

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip install -r /opt/odoo/odoo/requirements.txt

COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip install -r ${BUILD_ENVIRONMENT}.txt

RUN mkdir -p /etc/odoo \
    && mkdir -p /opt/odoo/data

COPY ./compose/odoo/etc/odoo.conf /etc/odoo/odoo.conf 

COPY ./compose/odoo/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/odoo/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

RUN groupadd --gid 1000 odoo \
    && useradd --uid 1000 --gid odoo --shell /bin/bash --create-home odoo \
    && echo odoo ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/odoo \
    && chmod 0440 /etc/sudoers.d/odoo

RUN chown -R odoo:odoo /etc/odoo \
    && chown -R odoo:odoo /opt/odoo 

USER odoo

ENTRYPOINT ["/entrypoint"]