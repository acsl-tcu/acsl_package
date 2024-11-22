#! /usr/bin/bash
# $(echo "exec rpicam-vid -t 0 --inline --listen -o tcp://0.0.0.0:5555")
/common/scripts/hostbash "rpicam-vid -t 0 --inline --listen -o tcp://0.0.0.0:5555"
