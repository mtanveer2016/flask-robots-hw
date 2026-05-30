from flask import Flask, render_template, request, jsonify
import time
import atexit

app = Flask(__name__)

print("\n" + "="*60)
print("🤖 ROBOT CONTROL SYSTEM")
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

# Initialize LED (but don't fail if it doesn't work)
led_available = False
try:
    LED = Led()
    led_available = True
    print("✅ LED initialized")
except Exception as e:
    print(f"⚠️ LED not available: {e}")
    LED = None

print("="*60 + "\n")

# ============================================
# Motor Control
# ============================================

def robot_forward():
    PWM.set_motor_model(1, 0, 1, 0)
    print("  🔴 FORWARD - Motors should move FORWARD")

def robot_backward():
    PWM.set_motor_model(0, 1, 0, 1)
    print("  🔴 BACKWARD - Motors should move BACKWARD")

def robot_left():
    PWM.set_motor_model(0, 1, 1, 0)
    print("  🔴 LEFT TURN - Robot should turn LEFT")

def robot_right():
    PWM.set_motor_model(1, 0, 0, 1)
    print("  🔴 RIGHT TURN - Robot should turn RIGHT")

def robot_stop():
    PWM.set_motor_model(0, 0, 0, 0)
    print("  ⚫ STOPPED - Motors should stop")

# ============================================
# LED Control (with error handling)
# ============================================

def led_feedback(color):
    """Provide LED feedback without crashing"""
    if not led_available or LED is None:
        print(f"  [INFO] LED would show: {color}")
        return
    
    try:
        # Try different methods
        if hasattr(LED, 'ledIndex') and callable(LED.ledIndex):
            if color == 'red':
                LED.ledIndex(0, 255, 0, 0)
            elif color == 'green':
                LED.ledIndex(0, 0, 255, 0)
            elif color == 'blue':
                LED.ledIndex(0, 0, 0, 255)
            elif color == 'off':
                LED.ledIndex(0, 0, 0, 0)
            print(f"  💡 LED: {color.upper()} (via ledIndex)")
        elif hasattr(LED, 'set_color') and callable(LED.set_color):
            if color == 'red':
                LED.set_color(255, 0, 0)
            elif color == 'green':
                LED.set_color(0, 255, 0)
            elif color == 'blue':
                LED.set_color(0, 0, 255)
            elif color == 'off':
                LED.set_color(0, 0, 0)
            print(f"  💡 LED: {color.upper()} (via set_color)")
        else:
            print(f"  [INFO] LED would show: {color} (no method found)")
    except Exception as e:
        print(f"  ⚠️ LED control failed: {e}")

# ============================================
# Flask Routes
# ============================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({
        'status': 'ok',
        'motor': 'connected',
        'led': led_available,
        'battery_warning': 'If motors hum but dont move, check battery voltage'
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    print(f"\n🤖 Robot {robot_id + 1}: {direction.upper()}")
    
    # LED feedback on movement
    if direction != 'stop':
        led_feedback('green')
    
    # Execute movement
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
        led_feedback('off')
    else:
        return jsonify({'error': 'Invalid direction'}), 400
    
    return jsonify({'status': 'ok', 'robot': robot_id, 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    return move_robot(0, direction)

@app.route("/led/test")
def led_test():
    """Test LED colors"""
    print("\n💡 LED TEST SEQUENCE")
    led_feedback('red')
    time.sleep(1)
    led_feedback('green')
    time.sleep(1)
    led_feedback('blue')
    time.sleep(1)
    led_feedback('off')
    return jsonify({'status': 'ok', 'message': 'LED test complete'})

# ============================================
# Cleanup
# ============================================

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    robot_stop()
    if led_available:
        led_feedback('off')
    PWM.close()
    print("✅ Cleanup complete")

if __name__ == "__main__":
    print("🚀 Starting server on port 5005")
    print("🌐 http://10.243.53.235:5005")
    print("\n⚠️  If motors hum but don't move:")
    print("   - Check battery voltage (needs 7.4V-12V)")
    print("   - Recharge or replace batteries")
    print("\n💡 If LED doesn't light:")
    print("   - Check 5V power to LED strip")
    print("   - Check data pin connection")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
