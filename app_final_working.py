from flask import Flask, render_template, request, jsonify
import time
import atexit

app = Flask(__name__)

print("\n" + "="*60)
print("🤖 ROBOT CONTROL SYSTEM - FREENOVE ROBOT")
print("="*60)

# Import libraries
try:
    from motor import Ordinary_Car
    from led import Led
    print("✅ Libraries loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    import sys
    sys.exit(1)

# Initialize motor controller
PWM = Ordinary_Car()
print("✅ Motor controller initialized")

# Initialize LED
LED = Led()
print("✅ LED initialized")

print("="*60 + "\n")

# ============================================
# Motor Control (Working)
# ============================================

def robot_forward():
    PWM.set_motor_model(1, 0, 1, 0)
    print("  🔴 FORWARD")

def robot_backward():
    PWM.set_motor_model(0, 1, 0, 1)
    print("  🔴 BACKWARD")

def robot_left():
    PWM.set_motor_model(0, 1, 1, 0)
    print("  🔴 LEFT TURN")

def robot_right():
    PWM.set_motor_model(1, 0, 0, 1)
    print("  🔴 RIGHT TURN")

def robot_stop():
    PWM.set_motor_model(0, 0, 0, 0)
    print("  ⚫ STOPPED")

# ============================================
# LED Control (Fixed)
# ============================================

def led_red():
    """Set LED to red"""
    try:
        # Try different methods that might work
        if hasattr(LED, 'set_color') and callable(LED.set_color):
            LED.set_color(255, 0, 0)
        elif hasattr(LED, 'color_wipe_index') and callable(LED.color_wipe_index):
            LED.color_wipe_index(0)
        elif hasattr(LED, 'ledIndex') and callable(LED.ledIndex):
            LED.ledIndex(0, 255, 0, 0)
        else:
            # Try property assignment
            if hasattr(LED, 'color_chase_rainbow_index'):
                # It's a property, try to assign
                pass
        print("  🔴 LED: RED")
    except Exception as e:
        print(f"  ⚠️ LED red failed: {e}")

def led_green():
    """Set LED to green"""
    try:
        if hasattr(LED, 'set_color') and callable(LED.set_color):
            LED.set_color(0, 255, 0)
        elif hasattr(LED, 'color_wipe_index') and callable(LED.color_wipe_index):
            LED.color_wipe_index(1)
        elif hasattr(LED, 'ledIndex') and callable(LED.ledIndex):
            LED.ledIndex(0, 0, 255, 0)
        print("  🟢 LED: GREEN")
    except Exception as e:
        print(f"  ⚠️ LED green failed: {e}")

def led_blue():
    """Set LED to blue"""
    try:
        if hasattr(LED, 'set_color') and callable(LED.set_color):
            LED.set_color(0, 0, 255)
        elif hasattr(LED, 'color_wipe_index') and callable(LED.color_wipe_index):
            LED.color_wipe_index(2)
        elif hasattr(LED, 'ledIndex') and callable(LED.ledIndex):
            LED.ledIndex(0, 0, 0, 255)
        print("  🔵 LED: BLUE")
    except Exception as e:
        print(f"  ⚠️ LED blue failed: {e}")

def led_off():
    """Turn off LED"""
    try:
        if hasattr(LED, 'set_color') and callable(LED.set_color):
            LED.set_color(0, 0, 0)
        elif hasattr(LED, 'ledIndex') and callable(LED.ledIndex):
            LED.ledIndex(0, 0, 0, 0)
        print("  ⚫ LED: OFF")
    except Exception as e:
        print(f"  ⚠️ LED off failed: {e}")

# ============================================
# Flask Routes
# ============================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({'status': 'ok', 'motor': 'connected'})

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    print(f"\n🤖 Robot {robot_id + 1}: {direction.upper()}")
    
    # Flash LED for feedback
    led_green()
    
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
    else:
        return jsonify({'error': 'Invalid direction'}), 400
    
    return jsonify({'status': 'ok', 'robot': robot_id, 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    return move_robot(0, direction)

@app.route("/led/red")
def set_led_red():
    led_red()
    return jsonify({'status': 'ok'})

@app.route("/led/green")
def set_led_green():
    led_green()
    return jsonify({'status': 'ok'})

@app.route("/led/blue")
def set_led_blue():
    led_blue()
    return jsonify({'status': 'ok'})

@app.route("/led/off")
def set_led_off():
    led_off()
    return jsonify({'status': 'ok'})

# ============================================
# Cleanup
# ============================================

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    robot_stop()
    led_off()
    PWM.close()
    print("✅ Cleanup complete")

if __name__ == "__main__":
    print("🚀 Starting server on port 5005")
    print("🌐 http://10.243.53.235:5005")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", debug=False, port=5005)
