#! /bin/bash
for i in $(seq 50000 50020)
do
	python sphere_server.py 192.168.71.4 $i &
done
