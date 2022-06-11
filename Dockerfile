# syntax=docker/dockerfile:1

FROM ubuntu:18.04 AS ubuntu

ENV PYTHON_VERSION 3.7.6
ENV PYTHON_PIP_VERSION 20.1
ENV DEBIAN_FRONTEND=noninteractive

# Ensure that the local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

## Install Python
RUN set -ex && apt-get -qqy update \
    # The dependencies that are required for Python build and run are taken from https://github.com/docker-library/python/blob/master/3.7/buster/slim/Dockerfile
    && apt-get -qqy install --no-install-recommends autoconf automake make unzip bzip2 dpkg-dev file gcc g++ libbz2-dev libc-dev \
    libc6-dev libcurl4-openssl-dev libdb-dev libevent-dev libgdbm-dev libglib2.0-dev libgmp-dev libkrb5-dev liblzma-dev \
    libmaxminddb-dev libncurses5-dev libncursesw5-dev libffi-dev libreadline-dev libsqlite3-dev libssl-dev libtool libwebp-dev \
    libxml2-dev libxslt-dev libyaml-dev patch tk-dev uuid-dev xz-utils zlib1g-dev ca-certificates gnupg libexpat-dev curl \
    && curl -sL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" --output python.tar.xz \
 && curl -sL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" --output python.tar.xz.asc \
 && export GNUPGHOME="$(mktemp -d)" \
 && gpg --batch --keyserver keys.openpgp.org --recv-keys "0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D" \
 && gpg --batch --verify python.tar.xz.asc python.tar.xz \
 && { command -v gpgconf > /dev/null && gpgconf --kill all || :; } \
 && rm -rf "$GNUPGHOME" python.tar.xz.asc \
 && mkdir -p /usr/src/python && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz && rm python.tar.xz \
 && cd /usr/src/python && gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
 && ./configure --build="$gnuArch" --enable-loadable-sqlite-extensions --enable-optimizations --enable-option-checking=fatal \
             --enable-shared --with-system-expat --with-system-ffi --without-ensurepip \
 && make -j "$(nproc)" \
  PROFILE_TASK='-m test.regrtest --pgo test_array test_base64 test_binascii test_binhex test_binop test_bytes \
   test_c_locale_coercion test_class test_cmath test_codecs test_compile test_complex test_csv test_decimal \
   test_dict test_float test_fstring test_hashlib test_io test_iter test_json test_long test_math \
   test_memoryview test_pickle test_re test_set test_slice test_struct test_threading test_time \
   test_traceback test_unicode' \
 && make install && ldconfig && find /usr/local -depth \
  \( \
   \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
   -o \
   \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
  \) -exec rm -rf '{}' + \
 && cd /usr/local/bin && ln -s idle3 idle && ln -s pydoc3 pydoc && ln -s python3 python && ln -s python3-config python-config \
 && rm -rf /usr/src/python && apt --purge -qqy remove autoconf automake make unzip gnupg && apt-get -qqy autoremove
## End install Python

## Install pip
RUN set -ex; curl -sL "https://github.com/pypa/get-pip/raw/1fe530e9e3d800be94e04f6428460fc4fb94f5a9/get-pip.py" --output get-pip.py; \
 python get-pip.py --disable-pip-version-check --no-cache-dir "pip==$PYTHON_PIP_VERSION"; \
 find /usr/local -depth \
  \( \
   \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
   -o \
   \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
  \) -exec rm -rf '{}' +; \
 rm -f get-pip.py
## End install pip

# Install system libraries
RUN apt-get update && apt-get install -y \
  apache2-utils \
  curl \
  expect \
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
  unzip \
  vim \
  wget \
  xvfb \
	gconf-service \
	libasound2 \ 
	libatk1.0-0 \
	libc6 \ 
	libcairo2 \ 
	libcups2 \
	libdbus-1-3 \
	libexpat1 \
	libfontconfig1 \
	libgcc1 \
	libgconf-2-4 \
	libgdk-pixbuf2.0-0 \
	libglib2.0-0 \
	libgtk-3-0 \
	libnspr4 \
	libpango-1.0-0 \
	libpangocairo-1.0-0 \
	libstdc++6 \
	libx11-6 \
	libx11-xcb1 \
	libxcb1 \
	libxcomposite1 \
	libxcursor1 \
	libxdamage1 \
	libxext6 \
	libxfixes3 \
	libxi6 \
	libxrandr2 \
	libxrender1 \
	libxss1 \
	libxtst6 \
	ca-certificates \
	fonts-liberation \
	libappindicator1 \
	libnss3 \
	lsb-release \
	xdg-utils \
  software-properties-common \
  libgbm1 \
  ## Remove temporary files.
  && rm -rf /var/log/* /var/lib/apt/lists/* \
  # Config ssh
  && mkdir -p /var/run/sshd /var/log/sshd var/log/lastlog/ \
  && sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config \
  && sed -i 's/#ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config  

# Install chromedriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_101.0.4951` && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver

# Install chrome
ENV CHROME_VERSION="101.0.4951.64-1"
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb
RUN ln -s /opt/google/chrome/google-chrome /usr/local/bin/google-chrome
# RUN chmod +x /usr/local/bin/google-chrome

# set chrome to start with --no-sandbox to root user
RUN sed -i 's/exec -a \"$0\" \"$HERE\/google-chrome\" \"$@\"/exec -a \"$0\" \"$HERE\/google-chrome\" \"$@\" --no-sandbox/g' /usr/local/bin/google-chrome

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

WORKDIR /opt

EXPOSE 443 22 4444 4445 9515

# Run app
Entrypoint ["/init.sh"]