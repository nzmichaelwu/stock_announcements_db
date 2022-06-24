#!/bin/bash

set -e

cron && tail -f /var/log/cron.log

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf