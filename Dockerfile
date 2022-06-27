# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

ENV DEBIAN_FRONTEND noninteractive
ENV GECKODRIVER_VER v0.31.0
ENV FIREFOX_VER 101.0

# Install system libraries
RUN apt-get update && apt-get install -y \
  apache2-utils \
  cron \
  curl \
  expect \
  firefox-esr \
  gdebi-core \
  gnupg \
  gnupg1 \
  gnupg2 \
  libcurl4-gnutls-dev \
  libsasl2-dev \
  python-dev \
  libldap2-dev \
  libssl-dev \
  nginx \
  protobuf-compiler \
  ssh \
  sssd \
  sssd-tools \
  supervisor \
  sudo \
  syslog-ng \
  tzdata \
  unzip \
  vim \
  wget \
  xvfb \
  ## Remove temporary files.
  && rm -rf /var/log/* /var/lib/apt/lists/* \
  # Config ssh
  && mkdir -p /var/run/sshd /var/log/sshd var/log/lastlog/ \
  && sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config \
  && sed -i 's/#ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config

COPY skel/post-install/etc/authorized_keys /root/.ssh/authorized_keys

# Set timezone to Sydney
ENV TZ=Australia/Sydney
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add latest FireFox
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/local/bin/

# Install required python packages
# copy the requirements.txt for python packages installation
COPY requirements.txt /opt/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/requirements.txt

# Copy relevant DB python files into the image
COPY ./db /opt/db

COPY skel/post-install/etc/authorized_keys /root/.ssh/authorized_keys

# Copy init.sh
COPY ./skel/post-install /
COPY ./skel/post-install/init.sh /init.sh

RUN chmod +x /init.sh

# Copy stock-ron file to the cron.d directory
COPY stock-cron /etc/cron.d/stock-cron
RUN chmod 0644 /etc/cron.d/stock-cron

# Apply cron job
RUN crontab /etc/cron.d/stock-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Create a folder called logs for all app logs
RUN mkdir -p /var/log/stockannouncementsdb
RUN mkdir -p /var/log/supervisor

# WORKDIR /opt

EXPOSE 22 4000 4444 9515 8000

# Run app
Entrypoint ["/init.sh"]
