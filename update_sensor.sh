#!/bin/bash

source /home/jphan32/.cache/pypoetry/virtualenvs/rack-monitor-rp-eOKCs1kn-py3.9/bin/activate
cd /data/rack-monitor-rp/
/home/jphan32/.local/bin/poetry run python update_sensor.py 
