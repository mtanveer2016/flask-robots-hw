from flask import Flask, request, jsonify
from motor import Ordinary_Car
import atexit

app = Flask(__name__)

# Initialize motor
PWM = Ordinary_Car()
print("✅ Robot Server Ready")

# Motor speed
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

@app.route("/move/<direction>")
def move(direction):
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
    return jsonify({'status': 'ok', 'direction': direction})

@atexit.register
def cleanup():
    robot_stop()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
