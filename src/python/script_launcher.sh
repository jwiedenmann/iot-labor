#!/bin/bash

if [ $(/bin/pgrep -f "jwiedenmann_iot_labor.py") ]; then
    echo "jwiedenmann_iot_labor running"
    python3.10 motorcycle_acceleration.py
else
    echo "jwiedenmann_iot_labor not running"
fi

# alle 10 Minuten
# */10 * * * * bash /home/wiedenmann/script_launcher.sh