#!/bin/bash
# Simple SHELL script for Linux and UNIX system monitoring with
# ping command
# -------------------------------------------------------------------------
# Copyright (c) 2006 nixCraft project <http://www.cyberciti.biz/fb/>
# This script is licensed under GNU GPL version 2.0 or above
# -------------------------------------------------------------------------
# This script is part of nixCraft shell script collection (NSSC)
# Visit http://bash.cyberciti.biz/ for more information.
# -------------------------------------------------------------------------
# Setup email ID below
# See URL for more info:
# http://www.cyberciti.biz/tips/simple-linux-and-unix-system-monitoring-with-ping-command-and-scripts.html
# -------------------------------------------------------------------------
 
# add ip / hostname separated by white space
HOSTS="www.google.com 192.168.0.69"
 
# no ping request
COUNT=5
INTERVAL=5

for myHost in $HOSTS
do
 ping -c 1 $myHost > /dev/null
 if [ $? -eq 0 ]; then 
  echo "Ping Failed"
 else
  echo "Ping Ok"
 fi
done
