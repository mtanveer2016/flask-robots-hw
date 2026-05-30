from flask import Flask, render_template, request, jsonify
import os
import RPi.GPIO as GPIO

app = Flask(__name__)

# ============================================
# CONFIGURATION
# ============================================
ROBOT_MODE = os.environ.get('ROBOT_MODE', 'REAL')
ROBOT_COUNT = int(os.environ.get('ROBOT_COUNT', '1'))

print(f"\n🚀 Starting Robot Control System")
print(f"   Mode: {ROBOT_MODE}")
print(f"   Robot Count: {ROBOT_COUNT}")

# ============================================
# GPIO Setup with RPi.GPIO
# ============================================
GPIO_AVAILABLE = False

if ROBOT_MODE == 'REAL':
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO_AVAILABLE = True
        print("✓ RPi.GPIO initialized successfully")
    except Exception as e:
        print(f"⚠️ GPIO error: {e}")

# ============================================
# Hardware Motor Class
# ============================================
class HardwareMotor:
    def __init__(self, pin):
        self.pin = pin
        self.working = False
        if GPIO_AVAILABLE:
            try:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
                self.working = True
                print(f"  ✅ GPIO {pin} initialized")
            except Exception as e:
                print(f"  ❌ Failed to init GPIO {pin}: {e}")
    
    def on(self):
        if self.working:
            GPIO.output(self.pin, GPIO.HIGH)
            print(f"  🔴 GPIO {self.pin} ON")
        else:
            print(f"  [MOCK] GPIO {self.pin} ON")
    
    def off(self):
        if self.working:
            GPIO.output(self.pin, GPIO.LOW)
            print(f"  ⚫ GPIO {self.pin} OFF")
        else:
            print(f"  [MOCK] GPIO {self.pin} OFF")

# ============================================
# Motor Pins
# ============================================
ROBOT_PINS = {
    0: {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
}

# Initialize motors
motors = {}
for robot_id in range(ROBOT_COUNT):
    pins = ROBOT_PINS.get(robot_id)
    if not pins:
        continue
        
    motors[robot_id] = {
        'in1': HardwareMotor(pins['in1']),
        'in2': HardwareMotor(pins['in2']),
        'in3': HardwareMotor(pins['in3']),
        'in4': HardwareMotor(pins['in4']),
    }
    
    # Stop all motors initially
    for motor in motors[robot_id].values():
        motor.off()
    
    print(f"✓ Robot {robot_id + 1} initialized")

# ============================================
# Motor Control
# ============================================
def set_motor_state(robot_id, in1_state, in2_state, in3_state, in4_state):
    if robot_id not in motors:
        return False
    
    motor = motors[robot_id]
    motor['in1'].on() if in1_state == 'on' else motor['in1'].off()
    motor['in2'].on() if in2_state == 'on' else motor['in2'].off()
    motor['in3'].on() if in3_state == 'on' else motor['in3'].off()
    motor['in4'].on() if in4_state == 'on' else motor['in4'].off()
    return True

# ============================================
# Flask Routes
# ============================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({
        'mode': ROBOT_MODE,
        'gpio_available': GPIO_AVAILABLE,
        'robots': len(motors)
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    if robot_id not in motors:
        return jsonify({'error': 'Robot not found'}), 404
    
    direction_map = {
        'forward': ('on', 'off', 'on', 'off'),
        'backward': ('off', 'on', 'off', 'on'),
        'left': ('off', 'on', 'on', 'off'),
        'right': ('on', 'off', 'off', 'on'),
        'stop': ('off', 'off', 'off', 'off'),
    }
    
    if direction not in direction_map:
        return jsonify({'error': 'Invalid direction'}), 400
    
    print(f"\n🤖 Robot {robot_id + 1}: {direction.upper()}")
    in1, in2, in3, in4 = direction_map[direction]
    set_motor_state(robot_id, in1, in2, in3, in4)
    
    return jsonify({'status': 'ok', 'robot': robot_id, 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    for robot_id in motors:
        move_robot(robot_id, direction)
    return jsonify({'status': 'ok', 'direction': direction})

# Cleanup on exit
import atexit
def cleanup():
    if GPIO_AVAILABLE:
        GPIO.cleanup()
        print("\n🧹 GPIO cleaned up")
atexit.register(cleanup)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 ROBOT CONTROL SYSTEM (RPi.GPIO)")
    print("="*60)
    print(f"🎮 Mode: {ROBOT_MODE}")
    print(f"📡 Server: http://localhost:5005")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", debug=False, port=5005)
