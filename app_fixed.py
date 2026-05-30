from flask import Flask, render_template, request, jsonify
from motor import Ordinary_Car
from buzzer import Buzzer
from led import Led
import threading
import time
import atexit

app = Flask(__name__)

print("\n" + "="*70)
print("🤖 MULTI-ROBOT CONTROL - USING WORKING MOTOR CONTROL")
print("="*70)

# Initialize hardware (same as working K8s app)
PWM = Ordinary_Car()
buzzer = Buzzer()
led = Led()

print("✅ Hardware initialized")

# ============================================
# MOTOR CONTROL - EXACT SAME AS WORKING APP
# ============================================
# Working app uses duty cycle values (0 to 4095)
# Positive = forward, Negative = backward

# Speed settings (match your working app)
FORWARD_SPEED = 2000
BACKWARD_SPEED = -2000
LEFT_SPEED = 2000   # For turning, one side positive, one negative
RIGHT_SPEED = 2000
TURN_SPEED = 2000

def robot_forward():
    """Move forward - using same values as working app"""
    PWM.set_motor_model(FORWARD_SPEED, FORWARD_SPEED, FORWARD_SPEED, FORWARD_SPEED)
    print(f"  🔴 FORWARD (speed: {FORWARD_SPEED})")

def robot_backward():
    """Move backward - using same values as working app"""
    PWM.set_motor_model(BACKWARD_SPEED, BACKWARD_SPEED, BACKWARD_SPEED, BACKWARD_SPEED)
    print(f"  🔴 BACKWARD (speed: {BACKWARD_SPEED})")

def robot_left():
    """Turn left - left backward, right forward"""
    PWM.set_motor_model(BACKWARD_SPEED, BACKWARD_SPEED, FORWARD_SPEED, FORWARD_SPEED)
    print(f"  🔴 LEFT TURN")

def robot_right():
    """Turn right - left forward, right backward"""
    PWM.set_motor_model(FORWARD_SPEED, FORWARD_SPEED, BACKWARD_SPEED, BACKWARD_SPEED)
    print(f"  🔴 RIGHT TURN")

def robot_stop():
    """Stop robot"""
    PWM.set_motor_model(0, 0, 0, 0)
    print("  ⚫ STOPPED")

def beep():
    try:
        buzzer.set_state(True)
        threading.Timer(0.1, lambda: buzzer.set_state(False)).start()
        print("  🔊 BEEP")
    except:
        pass

def led_on():
    try:
        led.ledIndex(0xFF, 255, 255, 255)
        print("  💡 LED ON")
    except:
        pass

def led_off():
    try:
        led.ledIndex(0xFF, 0, 0, 0)
        print("  💡 LED OFF")
    except:
        pass

# ============================================
# FLASK ROUTES
# ============================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({
        'status': 'ok',
        'mode': 'WORKING_MOTOR_CONTROL',
        'speed': FORWARD_SPEED
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    print(f"\n🤖 Command: {direction.upper()}")
    
    if direction != 'stop':
        beep()
        led_on()
    
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
        led_off()
    
    return jsonify({'status': 'ok', 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    return move_robot(0, direction)

@app.route("/speed/<int:speed>")
def set_speed(speed):
    global FORWARD_SPEED, BACKWARD_SPEED
    FORWARD_SPEED = speed
    BACKWARD_SPEED = -speed
    print(f"  ⚙️ Speed set to {speed}")
    return jsonify({'status': 'ok', 'speed': speed})

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    robot_stop()
    led_off()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 SERVER READY")
    print("="*70)
    print(f"📡 Web Interface: http://0.0.0.0:5005")
    print(f"🎮 Forward Speed: {FORWARD_SPEED}")
    print("\n💡 TIP: If robot doesn't move, try adjusting speed:")
    print("   http://localhost:5005/speed/3000  (higher speed)")
    print("   http://localhost:5005/speed/1000  (lower speed)")
    print("="*70 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
