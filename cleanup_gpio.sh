#!/bin/bash
echo "🧹 Force cleaning GPIO..."

# Kill all Python processes
sudo killall python3 python 2>/dev/null
sudo pkill -9 python
sudo pkill -9 python3

# Stop Kubernetes pods
kubectl scale deployment --all --replicas=0 -n default 2>/dev/null
kubectl scale deployment --all --replicas=0 -n staging 2>/dev/null

# Free GPIO pins
for pin in 13 21 17 27 22 23 24 25 18 19 20 26; do
    sudo sh -c "echo $pin > /sys/class/gpio/unexport" 2>/dev/null
done

# Close lgpio handles
sudo rm -f /tmp/lgpio-socket-* 2>/dev/null

# Restart lgpio
sudo systemctl restart lgpio 2>/dev/null
sudo systemctl restart pigpiod 2>/dev/null

sleep 2
echo "✅ Cleanup complete"
