
from flask import Flask, render_template, request, jsonify
import sys
import os
import atexit
import time

# Add the path to your Freenove libraries (adjust if needed)
# Usually the libraries are in the same directory as your main code
sys.path.append('/home/mtrobotcar/flask_robots_hw')

# Import Freenove robot car libraries
try:
    from motor import Ordinary_Car
    from buzzer import Buzzer
    from led import Led
    print("✅ Freenove libraries imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import Freenove libraries: {e}")
    print("   Make sure motor.py, buzzer.py, led.py are in the same directory")
    print("   Falling back to MOCK mode")
    
    # Mock classes for testing
    class Ordinary_Car:
        def __init__(self):
            print("  [MOCK] Car initialized")
        def forward(self):
            print("  [MOCK] Car moving FORWARD")
        def backward(self):
            print("  [MOCK] Car moving BACKWARD")
        def left(self):
            print("  [MOCK] Car turning LEFT")
        def right(self):
            print("  [MOCK] Car turning RIGHT")
        def stop(self):
            print("  [MOCK] Car STOPPED")
    
    class Buzzer:
        def __init__(self):
            print("  [MOCK] Buzzer initialized")
        def beep(self, duration=0.1):
            print(f"  [MOCK] BEEP (duration: {duration}s)")
    
    class Led:
        def __init__(self):
            print("  [MOCK] LED initialized")
        def on(self):
            print("  [MOCK] LED ON")
        def off(self):
            print("  [MOCK] LED OFF")

app = Flask(__name__)

# ============================================
# Hardware Initialization
# ============================================
print("\n" + "="*60)
print("🤖 ROBOT CONTROL SYSTEM - FREENOVE ROBOT CAR")
print("="*60)

# Initialize the robot car
try:
    PWM = Ordinary_Car()
    print("✅ Motor controller initialized")
except Exception as e:
    print(f"❌ Motor initialization failed: {e}")
    PWM = None

# Initialize buzzer
try:
    buzzer = Buzzer()
    print("✅ Buzzer initialized")
except Exception as e:
    print(f"⚠️ Buzzer initialization failed: {e}")
    buzzer = None

# Initialize LED
try:
    led = Led()
    print("✅ LED initialized")
except Exception as e:
    print(f"⚠️ LED initialization failed: {e}")
    led = None

print("="*60 + "\n")

# ============================================
# Robot Control Functions
# ============================================

def robot_forward():
    """Move robot forward"""
    if PWM:
        PWM.forward()
        print("  🔴 FORWARD")
    else:
        print("  [MOCK] FORWARD")

def robot_backward():
    """Move robot backward"""
    if PWM:
        PWM.backward()
        print("  🔴 BACKWARD")
    else:
        print("  [MOCK] BACKWARD")

def robot_left():
    """Turn robot left"""
    if PWM:
        PWM.left()
        print("  🔴 LEFT TURN")
    else:
        print("  [MOCK] LEFT")

def robot_right():
    """Turn robot right"""
    if PWM:
        PWM.right()
        print("  🔴 RIGHT TURN")
    else:
        print("  [MOCK] RIGHT")

def robot_stop():
    """Stop robot"""
    if PWM:
        PWM.stop()
        print("  ⚫ STOPPED")
    else:
        print("  [MOCK] STOP")

def robot_beep(duration=0.1):
    """Make robot beep"""
    if buzzer:
        buzzer.beep(duration)
        print(f"  🔊 BEEP (duration: {duration}s)")
    else:
        print(f"  [MOCK] BEEP")

def led_on():
    """Turn LED on"""
    if led:
        led.on()
        print("  💡 LED ON")
    else:
        print("  [MOCK] LED ON")

def led_off():
    """Turn LED off"""
    if led:
        led.off()
        print("  💡 LED OFF")
    else:
        print("  [MOCK] LED OFF")

# ============================================
# Flask Routes
# ============================================

@app.route("/")
def index():
    """Main page - serves the HTML interface"""
    return render_template("index.html")

@app.route("/status")
def status():
    """Get robot status"""
    return jsonify({
        'status': 'ok',
        'hardware': {
            'motor': PWM is not None,
            'buzzer': buzzer is not None,
            'led': led is not None
        },
        'mode': 'REAL' if PWM else 'MOCK'
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Control robot movement"""
    print(f"\n🤖 Robot {robot_id + 1}: {direction.upper()}")
    
    # Add visual feedback (beep and LED flash)
    if direction != 'stop':
        robot_beep(0.05)  # Quick beep on movement
        led_on()
    
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
        led_off()
    else:
        return jsonify({'error': 'Invalid direction'}), 400
    
    return jsonify({
        'status': 'ok',
        'robot': robot_id,
        'direction': direction,
        'hardware': PWM is not None
    })

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    """Control all robots (for multi-robot setup)"""
    return move_robot(0, direction)

@app.route("/beep")
def beep():
    """Make robot beep independently"""
    print("\n🔊 BEEP COMMAND")
    robot_beep(0.2)
    return jsonify({'status': 'ok', 'action': 'beep'})

@app.route("/led/<state>")
def set_led(state):
    """Control LED independently"""
    print(f"\n💡 LED: {state.upper()}")
    if state == 'on':
        led_on()
    elif state == 'off':
        led_off()
    else:
        return jsonify({'error': 'Invalid state'}), 400
    return jsonify({'status': 'ok', 'led': state})

@app.route("/dance")
def dance():
    """Make the robot dance!"""
    print("\n💃🕺 DANCE ROUTINE STARTED!")
    
    # Flash LED and beep to start
    for _ in range(3):
        led_on()
        robot_beep(0.1)
        time.sleep(0.1)
        led_off()
        time.sleep(0.1)
    
    # Dance steps
    dance_moves = [
        ('forward', 0.5),
        ('backward', 0.5),
        ('left', 0.3),
        ('right', 0.3),
        ('forward', 0.4),
        ('backward', 0.4),
        ('left', 0.3),
        ('right', 0.3),
        ('stop', 0.2)
    ]
    
    for move, duration in dance_moves:
        print(f"  💃 {move.upper()}")
        if move == 'forward':
            robot_forward()
        elif move == 'backward':
            robot_backward()
        elif move == 'left':
            robot_left()
        elif move == 'right':
            robot_right()
        elif move == 'stop':
            robot_stop()
        
        time.sleep(duration)
    
    # Final beep
    robot_beep(0.3)
    print("🎉 DANCE COMPLETE!")
    
    return jsonify({'status': 'ok', 'action': 'dance'})

@app.route("/speed/<int:robot_id>/<int:speed>")
def set_speed(robot_id, speed):
    """Set robot speed (if supported by your Freenove library)"""
    print(f"\n⚙️ Robot {robot_id + 1} speed = {speed}/10")
    
    # If your Freenove library supports speed control, add it here
    # For example:
    # if PWM:
    #     PWM.set_speed(speed)
    
    return jsonify({
        'status': 'ok',
        'robot': robot_id,
        'speed': speed,
        'note': 'Speed adjustment may require additional PWM configuration'
    })

# ============================================
# Health Check for Kubernetes
# ============================================

@app.route("/health")
def health():
    """Kubernetes health check"""
    return jsonify({
        'status': 'healthy',
        'hardware': {
            'motor': PWM is not None,
            'buzzer': buzzer is not None,
            'led': led is not None
        }
    })

@app.route("/ready")
def ready():
    """Kubernetes readiness check"""
    return jsonify({'ready': True})

# ============================================
# Cleanup on Exit
# ============================================

@atexit.register
def cleanup():
    """Clean up hardware on exit"""
    print("\n🧹 Cleaning up hardware...")
    
    # Stop the car
    if PWM:
        try:
            PWM.stop()
            print("  ✅ Car stopped")
        except:
            pass
    
    # Turn off LED
    if led:
        try:
            led.off()
            print("  ✅ LED turned off")
        except:
            pass
    
    # Final beep
    if buzzer:
        try:
            buzzer.beep(0.1)
            print("  ✅ Farewell beep")
        except:
            pass
    
    print("✅ Hardware cleanup complete")

# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 STARTING ROBOT CONTROL SERVER")
    print("="*60)
    print(f"📡 Web Interface: http://localhost:5005")
    print(f"🌐 External Access: http://10.243.53.235:5005")
    print("\n🎮 Available Commands:")
    print("   - /move/0/forward  - Move forward")
    print("   - /move/0/backward - Move backward")
    print("   - /move/0/left     - Turn left")
    print("   - /move/0/right    - Turn right")
    print("   - /move/0/stop     - Stop")
    print("   - /beep            - Make robot beep")
    print("   - /led/on          - Turn LED on")
    print("   - /led/off         - Turn LED off")
    print("   - /dance           - Dance routine!")
    print("="*60 + "\n")
    
    # Run the Flask app
    app.run(host="0.0.0.0", debug=False, port=5005)
