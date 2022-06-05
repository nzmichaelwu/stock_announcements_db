# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

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
  ## Remove temporary files.
  && rm -rf /var/log/* /var/lib/apt/lists/* \
  # Config ssh
  && mkdir -p /var/run/sshd /var/log/sshd var/log/lastlog/ \
  && sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config \
  && sed -i 's/#ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config  

COPY skel/post-install/etc/authorized_keys /root/.ssh/authorized_keys

# Install Google Chrome and Chrome Driver
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Updating apt to see and install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

# Install Heroku CLI onto the docker image
RUN apt-get update
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install required python packages
# copy the requirements.txt for python packages installation
COPY requirements.txt /opt/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/requirements.txt

# Copy relevant DB python files into the image
COPY ./db /opt/db

# Copy init.sh
COPY ./skel/post-install /
COPY ./skel/post-install/init.sh /init.sh

RUN chmod +x /init.sh
RUN chmod +x /heroku_login.exp
RUN chmod +x /heroku_login.sh

WORKDIR /opt

EXPOSE 443 22 4444 4445

# Run app
Entrypoint ["/init.sh"]