#!/bin/sh
#

sudo modprobe vcan
sudo ip link add dev can0 type vcan
sudo ip link set up can0
sudo ifconfig can0 txqueuelen 1000 up

sudo modprobe vcan
sudo ip link add dev can1 type vcan
sudo ip link set up can1
sudo ifconfig can1 txqueuelen 1000 up