#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import lgpio
import atexit

app = Flask(__name__)

print("\n" + "="*60)
print("🤖 ROBOT CONTROL - NO WIRE MOVE NEEDED")
print("="*60)

# Using GPIO 23 instead of 17 (both are free, but 23 may already have a wire?)
IN1 = 13  # Left motor forward
IN2 = 21  # Left motor backward
IN3 = 23  # Right motor forward (using GPIO 23 instead of 17)
IN4 = 27  # Right motor backward

print(f"📊 Pin Configuration:")
print(f"   Left Motor:  Forward=GPIO{IN1}, Backward=GPIO{IN2}")
print(f"   Right Motor: Forward=GPIO{IN3}, Backward=GPIO{IN4}")
print("="*60)

# Initialize GPIO
handle = lgpio.gpiochip_open(0)
print("✅ GPIO chip opened")

for pin in [IN1, IN2, IN3, IN4]:
    try:
        lgpio.gpio_claim_output(handle, pin)
        lgpio.gpio_write(handle, pin, 0)
        print(f"✅ GPIO {pin} initialized")
    except Exception as e:
        print(f"❌ GPIO {pin} failed: {e}")

print("\n🚀 Robot ready!")
print("="*60 + "\n")

def set_motors(in1, in2, in3, in4):
    lgpio.gpio_write(handle, IN1, 1 if in1 else 0)
    lgpio.gpio_write(handle, IN2, 1 if in2 else 0)
    lgpio.gpio_write(handle, IN3, 1 if in3 else 0)
    lgpio.gpio_write(handle, IN4, 1 if in4 else 0)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    print(f"\n🤖 Command: {direction.upper()}")
    
    if direction == 'forward':
        set_motors(1, 0, 1, 0)
        print("  ✅ FORWARD")
    elif direction == 'backward':
        set_motors(0, 1, 0, 1)
        print("  ✅ BACKWARD")
    elif direction == 'left':
        set_motors(0, 1, 1, 0)
        print("  ✅ LEFT")
    elif direction == 'right':
        set_motors(1, 0, 0, 1)
        print("  ✅ RIGHT")
    elif direction == 'stop':
        set_motors(0, 0, 0, 0)
        print("  ✅ STOP")
    
    return jsonify({'status': 'ok', 'direction': direction})

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    set_motors(0, 0, 0, 0)
    for pin in [IN1, IN2, IN3, IN4]:
        try:
            lgpio.gpio_free(handle, pin)
        except:
            pass
    lgpio.gpiochip_close(handle)
    print("✅ Cleanup complete")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5005)
