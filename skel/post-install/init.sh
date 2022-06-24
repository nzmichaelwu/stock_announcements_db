#!/bin/bash

set -e

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf

# cron && tail -f /var/log/cron.log
