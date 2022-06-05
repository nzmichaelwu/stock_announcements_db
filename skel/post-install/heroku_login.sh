#!/bin/bash

echo "attempt to login to heroku..."
expect /heroku_login.exp

echo
sleep 2

if heroku whoami ; then
  echo "heroku login successfully..."
else
  echo "heroku login unsuccesfully!"
fi
