# app_multi.py - Same beautiful UI, but routes to multiple robots
from flask import Flask, render_template, request, jsonify
from motor import Ordinary_Car
import requests
import threading

app = Flask(__name__)

# Robot configuration
ROBOTS = {
    0: {'name': 'Robot 1', 'ip': 'localhost', 'port': 5005, 'local': True},
    1: {'name': 'Robot 2', 'ip': '192.168.1.102', 'port': 5005, 'local': False},
    2: {'name': 'Robot 3', 'ip': '192.168.1.103', 'port': 5005, 'local': False},
    # Add more robots as you add them
}

# Local motor controller (for Robot 1)
PWM = Ordinary_Car()
SPEED = 2000

def robot_forward():
    PWM.set_motor_model(SPEED, SPEED, SPEED, SPEED)

def robot_backward():
    PWM.set_motor_model(-SPEED, -SPEED, -SPEED, -SPEED)

def robot_left():
    PWM.set_motor_model(-SPEED, -SPEED, SPEED, SPEED)

def robot_right():
    PWM.set_motor_model(SPEED, SPEED, -SPEED, -SPEED)

def robot_stop():
    PWM.set_motor_model(0, 0, 0, 0)

@app.route("/")
def index():
    # Your beautiful HTML with all 10 robot cards
    return render_template("index.html")

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Route command to the correct robot"""
    
    if robot_id not in ROBOTS:
        return jsonify({'error': 'Robot not found'}), 404
    
    robot = ROBOTS[robot_id]
    
    if robot['local']:
        # Control local robot directly
        if direction == 'forward':
            robot_forward()
        elif direction == 'backward':
            robot_backward()
        elif direction == 'left':
            robot_left()
        elif direction == 'right':
            robot_right()
        elif direction == 'stop':
            robot_stop()
        print(f"?? {robot['name']}: {direction} (LOCAL)")
    else:
        # Send command to remote robot
        try:
            url = f"http://{robot['ip']}:{robot['port']}/move/{direction}"
            requests.get(url, timeout=1)
            print(f"?? {robot['name']}: {direction} (REMOTE at {robot['ip']})")
        except Exception as e:
            print(f"? {robot['name']} failed: {e}")
            return jsonify({'error': 'Robot not reachable'}), 503
    
    return jsonify({'status': 'ok', 'robot': robot_id, 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    """Control all robots simultaneously"""
    print(f"\n?? ALL ROBOTS: {direction.upper()}")
    
    for robot_id in ROBOTS:
        move_robot(robot_id, direction)
    
    return jsonify({'status': 'ok', 'direction': direction})

@app.route("/dance")
def dance():
    """Sync dance with all robots"""
    print("\n???? SYNC DANCE WITH ALL ROBOTS!")
    
    dance_steps = [
        ('forward', 0.4), ('backward', 0.4),
        ('left', 0.3), ('right', 0.3),
        ('forward', 0.3), ('backward', 0.3),
        ('stop', 0.2),
    ]
    
    def execute_dance():
        for direction, duration in dance_steps:
            move_all_robots(direction)
            time.sleep(duration)
        move_all_robots('stop')
    
    thread = threading.Thread(target=execute_dance)
    thread.start()
    
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    print("\n" + "="*60)
    print("?? MULTI-ROBOT CONTROL - BEAUTIFUL UI")
    print("="*60)
    print(f"?? Web Interface: http://0.0.0.0:5005")
    print(f"?? Configured Robots: {len(ROBOTS)}")
    for rid, robot in ROBOTS.items():
        print(f"   Robot {rid}: {robot['name']} at {robot['ip']}")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
