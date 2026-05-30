from flask import Flask, render_template, request, jsonify
from gpiozero import OutputDevice
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory
import atexit
import time
import os

app = Flask(__name__)

print("\n" + "="*60)
print("🤖 ROBOT CONTROL SYSTEM - RESILIENT MODE")
print("="*60)

# Setup for Pi 5
Device.pin_factory = LGPIOFactory()

# Try to initialize each pin individually with retries
def init_pin(pin, retries=3):
    for attempt in range(retries):
        try:
            device = OutputDevice(pin, initial_value=False)
            return device
        except Exception as e:
            print(f"  Attempt {attempt+1}: GPIO {pin} failed - {e}")
            time.sleep(1)
    return None

print("\nInitializing GPIO pins...")
IN1 = init_pin(13)  # Left motor forward
IN2 = init_pin(21)  # Left motor backward
IN3 = init_pin(17)  # Right motor forward
IN4 = init_pin(27)  # Right motor backward

# Check which pins are working
working_pins = []
if IN1: working_pins.append(13)
if IN2: working_pins.append(21)
if IN3: working_pins.append(17)
if IN4: working_pins.append(27)

print(f"\n✅ Working pins: {working_pins}")

if len(working_pins) < 4:
    print(f"⚠️ Warning: Only {len(working_pins)}/4 pins are working")
    print("   Robot movement may be limited")

print("="*60 + "\n")

def set_motors(left_fwd, left_bwd, right_fwd, right_bwd):
    if IN1:
        IN1.on() if left_fwd else IN1.off()
    if IN2:
        IN2.on() if left_bwd else IN2.off()
    if IN3:
        IN3.on() if right_fwd else IN3.off()
    if IN4:
        IN4.on() if right_bwd else IN4.off()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({
        'status': 'ok',
        'mode': 'REAL',
        'working_pins': working_pins,
        'gpio_count': len(working_pins)
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    print(f"\n🤖 Robot {robot_id + 1}: {direction.upper()}")
    
    if direction == 'forward':
        set_motors(True, False, True, False)
        print("  ✅ Moving FORWARD")
        
    elif direction == 'backward':
        set_motors(False, True, False, True)
        print("  ✅ Moving BACKWARD")
        
    elif direction == 'left':
        set_motors(False, True, True, False)
        print("  ✅ Turning LEFT")
        
    elif direction == 'right':
        set_motors(True, False, False, True)
        print("  ✅ Turning RIGHT")
        
    elif direction == 'stop':
        set_motors(False, False, False, False)
        print("  ✅ STOPPED")
    
    return jsonify({'status': 'ok', 'robot': robot_id, 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    return move_robot(0, direction)

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    set_motors(False, False, False, False)
    for device in [IN1, IN2, IN3, IN4]:
        if device:
            try:
                device.close()
            except:
                pass

if __name__ == "__main__":
    print("🚀 Starting server on port 5005")
    print("🌐 Open http://localhost:5005 in your browser")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", debug=False, port=5005)
