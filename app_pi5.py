from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)

# ============================================
# CONFIGURATION
# ============================================
ROBOT_MODE = os.environ.get('ROBOT_MODE', 'REAL')
USE_GPIO = os.environ.get('USE_GPIO', 'true').lower() == 'true'
ROBOT_COUNT = int(os.environ.get('ROBOT_COUNT', '1'))

print(f"\n🚀 Starting Robot Control System")
print(f"   Mode: {ROBOT_MODE}")
print(f"   Robot Count: {ROBOT_COUNT}")
print(f"   GPIO Enabled: {USE_GPIO}")

# ============================================
# GPIO Setup with gpiozero (Pi 5 compatible)
# ============================================
GPIO_AVAILABLE = False

if ROBOT_MODE == 'REAL' and USE_GPIO:
    try:
        from gpiozero import OutputDevice
        from gpiozero import Device
        from gpiozero.pins.lgpio import LGPIOFactory
        
        # Use lgpio factory for Pi 5 compatibility
        Device.pin_factory = LGPIOFactory()
        GPIO_AVAILABLE = True
        print("✓ gpiozero with lgpio initialized successfully (Pi 5 compatible)")
    except ImportError as e:
        print(f"⚠️ gpiozero not installed: {e}")
        print("   Install with: sudo apt install python3-gpiozero")
    except Exception as e:
        print(f"⚠️ GPIO error: {e}")

# ============================================
# Hardware Motor Class using gpiozero
# ============================================
class HardwareMotor:
    def __init__(self, pin):
        self.pin = pin
        self.device = None
        if GPIO_AVAILABLE:
            try:
                self.device = OutputDevice(pin, initial_value=False)
                print(f"  ✅ GPIO {pin} initialized")
            except Exception as e:
                print(f"  ❌ Failed to init GPIO {pin}: {e}")
    
    def on(self):
        if self.device:
            self.device.on()
            print(f"  🔴 GPIO {self.pin} ON")
        else:
            print(f"  [MOCK] GPIO {self.pin} ON")
    
    def off(self):
        if self.device:
            self.device.off()
            print(f"  ⚫ GPIO {self.pin} OFF")
        else:
            print(f"  [MOCK] GPIO {self.pin} OFF")

# ============================================
# Motor Pins (BCM numbering)
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
# Motor Control Functions
# ============================================
def set_motor_state(robot_id, in1_state, in2_state, in3_state, in4_state):
    if robot_id not in motors:
        return False
    
    motor = motors[robot_id]
    
    if in1_state == 'on':
        motor['in1'].on()
    else:
        motor['in1'].off()
        
    if in2_state == 'on':
        motor['in2'].on()
    else:
        motor['in2'].off()
        
    if in3_state == 'on':
        motor['in3'].on()
    else:
        motor['in3'].off()
        
    if in4_state == 'on':
        motor['in4'].on()
    else:
        motor['in4'].off()
    
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

@app.route("/speed/<int:robot_id>/<int:speed>")
def set_speed(robot_id, speed):
    print(f"⚙️ Robot {robot_id + 1} speed = {speed}/10")
    return jsonify({'status': 'ok', 'robot': robot_id, 'speed': speed})

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 ROBOT CONTROL SYSTEM (Pi 5 - gpiozero)")
    print("="*60)
    print(f"🎮 Mode: {ROBOT_MODE}")
    print(f"📡 Server: http://localhost:5005")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", debug=False, port=5005)

