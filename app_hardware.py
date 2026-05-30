# app_hardware.py - Single Robot Version for Kubernetes
from flask import Flask, render_template, request, jsonify
import os
import sys

app = Flask(__name__)

# ============================================
# CONFIGURATION - Read from Environment Variables
# ============================================
ROBOT_MODE = os.environ.get('ROBOT_MODE', 'MOCK')  # MOCK or REAL
ROBOT_COUNT = int(os.environ.get('ROBOT_COUNT', '1'))  # Start with 1
USE_GPIO = os.environ.get('USE_GPIO', 'false').lower() == 'true'

print(f"\n🚀 Starting Robot Control System")
print(f"   Mode: {ROBOT_MODE}")
print(f"   Robot Count: {ROBOT_COUNT}")
print(f"   GPIO Enabled: {USE_GPIO}")

# ============================================
# GPIO Setup (Only if in REAL mode)
# ============================================
try:
    from gpiozero import OutputDevice
    from gpiozero.pins.pigpio import PiGPIOFactory
    GPIO_AVAILABLE = True
    print("✓ GPIO library loaded successfully")
except ImportError:
    GPIO_AVAILABLE = False
    print("⚠️ GPIO library not available - using mock mode")

# Motor pin definitions for each robot
# Each robot needs 4 pins (IN1, IN2, IN3, IN4)
ROBOT_PINS = {
    0: {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},   # Robot 1
    # Add more robots here as you expand
    # 1: {'in1': 14, 'in2': 15, 'in3': 18, 'in4': 23},  # Robot 2
    # 2: {'in1': 24, 'in2': 25, 'in3': 8, 'in4': 7},    # Robot 3
}

# ============================================
# Hardware Motor Class (Real GPIO)
# ============================================
class HardwareMotor:
    def __init__(self, pin, factory=None):
        self.pin = pin
        self.factory = factory
        self.device = None
        
    def init_device(self):
        if GPIO_AVAILABLE and USE_GPIO:
            try:
                if self.factory:
                    self.device = OutputDevice(self.pin, pin_factory=self.factory)
                else:
                    self.device = OutputDevice(self.pin)
                return True
            except Exception as e:
                print(f"  ❌ Failed to initialize GPIO {self.pin}: {e}")
                return False
        return False
    
    def on(self):
        if self.device:
            self.device.on()
            print(f"  🔌 GPIO {self.pin} ON")
        else:
            print(f"  [MOCK] GPIO {self.pin} ON")
    
    def off(self):
        if self.device:
            self.device.off()
            print(f"  🔌 GPIO {self.pin} OFF")
        else:
            print(f"  [MOCK] GPIO {self.pin} OFF")

# ============================================
# Initialize Motors
# ============================================
motors = {}

if ROBOT_MODE == 'REAL' and GPIO_AVAILABLE and USE_GPIO:
    print("\n🔌 Initializing REAL hardware mode...")
    
    # For Kubernetes on Raspberry Pi, pigpiod needs to be running
    # Create connection to local pigpio daemon
    factory = None
    try:
        # Connect to pigpio daemon on localhost (port 8888)
        factory = PiGPIOFactory(host='127.0.0.1')
        print("✓ Connected to pigpio daemon on localhost")
    except Exception as e:
        print(f"⚠️ Could not connect to pigpio: {e}")
        print("   Falling back to direct GPIO (may need sudo)")
    
    for robot_id in range(ROBOT_COUNT):
        pins = ROBOT_PINS.get(robot_id)
        if not pins:
            print(f"⚠️ No pins defined for Robot {robot_id + 1}")
            continue
            
        motors[robot_id] = {
            'in1': HardwareMotor(pins['in1'], factory),
            'in2': HardwareMotor(pins['in2'], factory),
            'in3': HardwareMotor(pins['in3'], factory),
            'in4': HardwareMotor(pins['in4'], factory),
        }
        
        # Initialize each motor device
        for motor in motors[robot_id].values():
            motor.init_device()
        
        # Stop all motors initially (safety)
        motors[robot_id]['in1'].off()
        motors[robot_id]['in2'].off()
        motors[robot_id]['in3'].off()
        motors[robot_id]['in4'].off()
        
        print(f"✓ Robot {robot_id + 1} initialized on pins: {pins}")
    
    print(f"✅ Initialized {len(motors)} REAL robot(s)")

else:
    print("\n🎮 Running in MOCK mode (no hardware)")
    for robot_id in range(ROBOT_COUNT):
        motors[robot_id] = {
            'in1': HardwareMotor(13 + robot_id),
            'in2': HardwareMotor(21 + robot_id),
            'in3': HardwareMotor(17 + robot_id),
            'in4': HardwareMotor(27 + robot_id),
        }
    print(f"✅ Initialized {len(motors)} MOCK robot(s)")

# ============================================
# Motor Control Functions
# ============================================
def set_motor_state(robot_id, in1_state, in2_state, in3_state, in4_state):
    """Set motor states for a specific robot"""
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
    """Get system status"""
    return jsonify({
        'mode': ROBOT_MODE,
        'robots': len(motors),
        'gpio_available': GPIO_AVAILABLE,
        'use_gpio': USE_GPIO
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Control a specific robot"""
    if robot_id not in motors:
        return jsonify({'error': f'Robot {robot_id} not found'}), 404
    
    direction_symbols = {
        'forward': '⬆️ FORWARD',
        'backward': '⬇️ BACKWARD', 
        'left': '⬅️ LEFT',
        'right': '➡️ RIGHT',
        'stop': '🛑 STOP'
    }
    
    print(f"\n🤖 Robot {robot_id + 1}: {direction_symbols.get(direction, direction)}")
    
    if direction == 'forward':
        # Left motor forward, Right motor forward
        set_motor_state(robot_id, 'on', 'off', 'on', 'off')
        
    elif direction == 'backward':
        # Left motor backward, Right motor backward
        set_motor_state(robot_id, 'off', 'on', 'off', 'on')
        
    elif direction == 'left':
        # Turn left: Left motor backward, Right motor forward
        set_motor_state(robot_id, 'off', 'on', 'on', 'off')
        
    elif direction == 'right':
        # Turn right: Left motor forward, Right motor backward
        set_motor_state(robot_id, 'on', 'off', 'off', 'on')
        
    elif direction == 'stop':
        # All motors off
        set_motor_state(robot_id, 'off', 'off', 'off', 'off')
        
    else:
        return jsonify({'error': 'Invalid direction'}), 400
    
    return jsonify({
        'status': 'ok', 
        'robot': robot_id, 
        'direction': direction,
        'mode': ROBOT_MODE
    })

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    """Control all robots at once"""
    print(f"\n🌐 GLOBAL: All robots {direction.upper()}")
    for robot_id in motors:
        move_robot(robot_id, direction)
    return jsonify({
        'status': 'ok', 
        'direction': direction, 
        'robots': len(motors),
        'mode': ROBOT_MODE
    })

@app.route("/speed/<int:robot_id>/<int:speed>")
def set_speed(robot_id, speed):
    """Set speed (PWM) for a robot"""
    if robot_id not in motors:
        return jsonify({'error': 'Robot not found'}), 404
    
    print(f"  ⚙️ Robot {robot_id + 1} speed = {speed}/10")
    
    # Note: For real PWM control, you'd use PWMOutputDevice
    # For now, we just log the speed setting
    
    return jsonify({'status': 'ok', 'robot': robot_id, 'speed': speed})

# ============================================
# Health Check for Kubernetes
# ============================================
@app.route("/health")
def health():
    """Kubernetes health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'mode': ROBOT_MODE,
        'robots': len(motors)
    })

@app.route("/ready")
def ready():
    """Kubernetes readiness check endpoint"""
    return jsonify({
        'ready': True,
        'robots_initialized': len(motors)
    })

# ============================================
# Main Entry Point
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 SINGLE ROBOT CONTROL SYSTEM (Hardware Ready)")
    print("="*60)
    print(f"🎮 Mode: {ROBOT_MODE}")
    print(f"📡 Server: http://localhost:5005")
    print(f"🔌 GPIO: {'Enabled' if USE_GPIO else 'Disabled'}")
    print("\n💡 To switch to REAL hardware:")
    print("   Set environment: ROBOT_MODE=REAL USE_GPIO=true")
    print("="*60 + "\n")
    
    # For Kubernetes, bind to 0.0.0.0
    app.run(host="0.0.0.0", debug=False, port=5005)