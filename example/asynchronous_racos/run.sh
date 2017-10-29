#! /bin/bash
for i in $(seq 50000 50002)
do
	python sphere_server.py 127.0.0.1 $i &
done
