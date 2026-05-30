from flask import Flask, render_template, request, jsonify
import time
import atexit

app = Flask(__name__)

# ============================================
# Hardware Initialization
# ============================================
print("\n" + "="*60)
print("🤖 ROBOT CONTROL SYSTEM - FREENOVE ROBOT")
print("="*60)

# Import Freenove libraries
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

# Initialize LED strip
LED = Led()
print("✅ LED strip initialized")

# Set default motor speed (duty cycle range: 0-100)
DEFAULT_SPEED = 50

print("="*60 + "\n")

# ============================================
# Motor Control Functions
# ============================================

def set_motor_speed(speed):
    """Set motor speed (0-100)"""
    speed = max(0, min(100, speed))
    PWM.pwm.set_dutycycle(speed)
    print(f"  ⚙️ Speed set to {speed}%")

def robot_forward():
    """Move robot forward"""
    # set_motor_model(left_upper, left_lower, right_upper, right_lower)
    # Positive values = forward, Negative values = backward
    # For forward: left_upper=1, left_lower=0, right_upper=1, right_lower=0
    PWM.set_motor_model(1, 0, 1, 0)
    print("  🔴 FORWARD")

def robot_backward():
    """Move robot backward"""
    # For backward: left_upper=0, left_lower=1, right_upper=0, right_lower=1
    PWM.set_motor_model(0, 1, 0, 1)
    print("  🔴 BACKWARD")

def robot_left():
    """Turn robot left"""
    # For left turn: left_upper=0, left_lower=1, right_upper=1, right_lower=0
    PWM.set_motor_model(0, 1, 1, 0)
    print("  🔴 LEFT TURN")

def robot_right():
    """Turn robot right"""
    # For right turn: left_upper=1, left_lower=0, right_upper=0, right_lower=1
    PWM.set_motor_model(1, 0, 0, 1)
    print("  🔴 RIGHT TURN")

def robot_stop():
    """Stop robot"""
    # All zeros to stop
    PWM.set_motor_model(0, 0, 0, 0)
    print("  ⚫ STOPPED")

# ============================================
# LED Control Functions (RGB Strip)
# ============================================

def led_red():
    """Set LED to red"""
    try:
        LED.color_chase_rainbow_index(0)  # Index 0 is usually red
        print("  🔴 LED: RED")
    except:
        print("  [MOCK] LED: RED")

def led_green():
    """Set LED to green"""
    try:
        LED.color_chase_rainbow_index(1)  # Index 1 is usually green
        print("  🟢 LED: GREEN")
    except:
        print("  [MOCK] LED: GREEN")

def led_blue():
    """Set LED to blue"""
    try:
        LED.color_chase_rainbow_index(2)  # Index 2 is usually blue
        print("  🔵 LED: BLUE")
    except:
        print("  [MOCK] LED: BLUE")

def led_rainbow():
    """Rainbow LED effect"""
    try:
        LED.rainbowCycle()
        print("  🌈 LED: RAINBOW")
    except:
        print("  [MOCK] LED: RAINBOW")

def led_off():
    """Turn off LED strip"""
    try:
        LED.ledIndex(0, 0, 0, 0)  # All off
        print("  ⚫ LED: OFF")
    except:
        print("  [MOCK] LED: OFF")

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
        'led': 'connected'
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    print(f"\n🤖 Robot {robot_id + 1}: {direction.upper()}")
    
    # Visual feedback - flash LED
    led_green()
    
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
    
    return jsonify({'status': 'ok', 'robot': robot_id, 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    return move_robot(0, direction)

@app.route("/led/red")
def set_led_red():
    led_red()
    return jsonify({'status': 'ok', 'color': 'red'})

@app.route("/led/green")
def set_led_green():
    led_green()
    return jsonify({'status': 'ok', 'color': 'green'})

@app.route("/led/blue")
def set_led_blue():
    led_blue()
    return jsonify({'status': 'ok', 'color': 'blue'})

@app.route("/led/rainbow")
def set_led_rainbow():
    led_rainbow()
    return jsonify({'status': 'ok', 'effect': 'rainbow'})

@app.route("/led/off")
def set_led_off():
    led_off()
    return jsonify({'status': 'ok', 'led': 'off'})

@app.route("/dance")
def dance():
    """Make the robot dance!"""
    print("\n💃🕺 DANCE ROUTINE STARTED!")
    
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
    
    # Rainbow LED finale
    led_rainbow()
    time.sleep(1)
    led_off()
    
    print("🎉 DANCE COMPLETE!")
    return jsonify({'status': 'ok', 'action': 'dance'})

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

# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 STARTING ROBOT CONTROL SERVER")
    print("="*60)
    print("📡 Web Interface: http://localhost:5005")
    print("🌐 External Access: http://10.243.53.235:5005")
    print("\n🎮 Available Commands:")
    print("   - /move/0/forward  - Move forward")
    print("   - /move/0/backward - Move backward")
    print("   - /move/0/left     - Turn left")
    print("   - /move/0/right    - Turn right")
    print("   - /move/0/stop     - Stop")
    print("   - /led/red         - LED red")
    print("   - /led/green       - LED green")
    print("   - /led/blue        - LED blue")
    print("   - /led/rainbow     - Rainbow effect")
    print("   - /led/off         - LED off")
    print("   - /dance           - Dance routine!")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
