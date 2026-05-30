#!/bin/bash

echo "========================================="
echo "Starting Robot Control System"
echo "========================================="

# Kill any existing Python processes using GPIO
echo "Cleaning up existing processes..."
sudo pkill -9 python
sudo pkill -9 python3
sudo pkill -9 sidecar
sudo pkill -9 wayvnc-control.py

# Wait for cleanup
sleep 2

# Free GPIO pins
echo "Freeing GPIO pins..."
for pin in 13 21 17 27; do
    sudo sh -c "echo $pin > /sys/class/gpio/unexport" 2>/dev/null
done

# Start the robot app
echo "Starting robot app..."
cd /home/mtrobotcar/flask_robots_hw
sudo python3 app_lgpio_final.py
