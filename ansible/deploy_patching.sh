#!/bin/bash
ansible-playbook -i ./inventory/servers.yml ./playbooks/weather_station_patching.yml
