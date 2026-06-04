#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "🤖 ROBOT CONTROL SWITCHER"
echo "========================================="

case "$1" in
    k8s)
        echo -e "${YELLOW}Switching to K8s app...${NC}"
        # Stop local app if running
        sudo pkill -9 python
        sudo pkill -9 python3
        # Start K8s app
        kubectl scale deployment flask-robot -n staging --replicas=1
        echo -e "${GREEN}✅ K8s app active on port 32391${NC}"
        echo "   Access at: http://10.202.105.234:32391"
        ;;
    local)
        echo -e "${YELLOW}Switching to Local app...${NC}"
        # Stop K8s app
        kubectl scale deployment flask-robot -n staging --replicas=0
        # Wait for pod to terminate
        echo "   Waiting for K8s pod to stop..."
        sleep 3
        # Start local app
        cd /home/mtrobotcar/flask_robots_hw
        echo -e "${GREEN}✅ Local app ready!${NC}"
        echo "   Run: sudo python3 app.py"
        ;;
    status)
        echo -e "${YELLOW}Current status:${NC}"
        echo -n "   K8s app: "
        kubectl get pods -n staging -l app=flask-robot 2>/dev/null | grep -q Running && echo -e "${GREEN}Running${NC}" || echo -e "${RED}Stopped${NC}"
        echo -n "   Local app: "
        pgrep -f "python.*app.py" > /dev/null && echo -e "${GREEN}Running${NC}" || echo -e "${RED}Stopped${NC}"
        ;;
    stop)
        echo -e "${YELLOW}Stopping all apps...${NC}"
        kubectl scale deployment flask-robot -n staging --replicas=0
        sudo pkill -9 python
        sudo pkill -9 python3
        echo -e "${GREEN}✅ All apps stopped${NC}"
        ;;
    *)
        echo "Usage: $0 {k8s|local|status|stop}"
        echo ""
        echo "  k8s    - Start Kubernetes app (stops local app)"
        echo "  local  - Prepare for local app (stops K8s app)"
        echo "  status - Show which app is running"
        echo "  stop   - Stop all apps"
        ;;
esac
