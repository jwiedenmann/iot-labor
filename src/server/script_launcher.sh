#!/bin/bash

if [ $(/bin/pgrep -f "jwiedenmann_iot_labor.py") ]; then
    echo "jwiedenmann_iot_labor running"
else
    echo "jwiedenmann_iot_labor not running"
    /usr/bin/python3.10 jwiedenmann_iot_labor.py
fi

# alle 10 Minuten
# */10 * * * * bash /home/wiedenmann/script_launcher.sh