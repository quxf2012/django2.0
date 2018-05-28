#!/bin/bash
set -x
sudo curl -X PUT  -d @unit.json --unix-socket /var/run/control.unit.sock http://localhost/

#python manage.py  collectstatic  
#sudo curl --unix-socket /var/run/control.unit.sock http://localhost/
