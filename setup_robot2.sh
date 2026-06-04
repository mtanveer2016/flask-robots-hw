#!/bin/bash
echo "Setting up Robot 2..."

# Install dependencies
sudo apt update
sudo apt install python3-pip -y
sudo pip3 install flask gpiozero lgpio

# Create app
cat > robot_server.py << 'END'
from flask import Flask, request, jsonify
from motor import Ordinary_Car
import atexit

app = Flask(__name__)
PWM = Ordinary_Car()
SPEED = 2000

@app.route("/move/<direction>")
def move(direction):
    if direction == 'forward':
        PWM.set_motor_model(SPEED, SPEED, SPEED, SPEED)
    elif direction == 'backward':
        PWM.set_motor_model(-SPEED, -SPEED, -SPEED, -SPEED)
    elif direction == 'left':
        PWM.set_motor_model(-SPEED, -SPEED, SPEED, SPEED)
    elif direction == 'right':
        PWM.set_motor_model(SPEED, SPEED, -SPEED, -SPEED)
    elif direction == 'stop':
        PWM.set_motor_model(0, 0, 0, 0)
    return jsonify({'status': 'ok'})

@atexit.register
def cleanup():
    PWM.set_motor_model(0, 0, 0, 0)

if __name__ == "__main__":
    print("Robot 2 Server Ready on port 5005")
    app.run(host="0.0.0.0", port=5005)
END

# Run
sudo python3 robot_server.py
