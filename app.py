from flask import Flask, render_template, request, jsonify
from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import socket
import time

app = Flask(__name__)

# ============================================
# CONFIGURATION FOR 10 ROBOTS WITH WIFI
# ============================================

# Each robot's Raspberry Pi IP address on your WiFi network
# IMPORTANT: Replace these with your actual Raspberry Pi IP addresses
ROBOT_CONFIG = {
    0: {
        'name': 'Robot 1',
        'ip': '192.168.1.101',      # Robot 1's Pi IP address
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},  # GPIO pins on Robot 1's Pi
        'status': 'offline'
    },
    1: {
        'name': 'Robot 2',
        'ip': '192.168.1.102',      # Robot 2's Pi IP address
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},  # Same pin numbers (each Pi has its own)
        'status': 'offline'
    },
    2: {
        'name': 'Robot 3',
        'ip': '192.168.1.103',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    },
    3: {
        'name': 'Robot 4',
        'ip': '192.168.1.104',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    },
    4: {
        'name': 'Robot 5',
        'ip': '192.168.1.105',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    },
    5: {
        'name': 'Robot 6',
        'ip': '192.168.1.106',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    },
    6: {
        'name': 'Robot 7',
        'ip': '192.168.1.107',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    },
    7: {
        'name': 'Robot 8',
        'ip': '192.168.1.108',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    },
    8: {
        'name': 'Robot 9',
        'ip': '192.168.1.109',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    },
    9: {
        'name': 'Robot 10',
        'ip': '192.168.1.110',
        'pins': {'in1': 13, 'in2': 21, 'in3': 17, 'in4': 27},
        'status': 'offline'
    }
}

# Global dictionary to store motor connections
motors = {}

# ============================================
# CONNECTION TESTING FUNCTION
# ============================================

def test_connection(ip, port=8888):
    """Test if a Raspberry Pi is reachable on the network"""
    try:
        socket.setdefaulttimeout(2)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip, port))
        return True
    except:
        return False

# ============================================
# INITIALIZE CONNECTIONS TO ALL ROBOTS
# ============================================

def init_robot_connections():
    """Establish connections to all Raspberry Pis over WiFi"""
    global motors
    
    print("\n" + "="*60)
    print("🔌 CONNECTING TO ROBOTS OVER WiFi")
    print("="*60)
    
    successful_connections = 0
    
    for robot_id, config in ROBOT_CONFIG.items():
        ip = config['ip']
        print(f"\n📡 Connecting to {config['name']} at {ip}...")
        
        # Test if Pi is reachable
        if test_connection(ip):
            try:
                # Create GPIO factory for this specific Raspberry Pi
                # PiGPIOFactory uses port 8889 by default, but we test port 8888 first
                factory = PiGPIOFactory(host=ip)
                
                # Create motor control objects using the GPIO pins on this robot's Pi
                pins = config['pins']
                motors[robot_id] = {
                    'in1': OutputDevice(pins['in1'], pin_factory=factory),
                    'in2': OutputDevice(pins['in2'], pin_factory=factory),
                    'in3': OutputDevice(pins['in3'], pin_factory=factory),
                    'in4': OutputDevice(pins['in4'], pin_factory=factory),
                    'ip': ip,
                    'connected': True
                }
                
                ROBOT_CONFIG[robot_id]['status'] = 'online'
                successful_connections += 1
                print(f"  ✅ {config['name']} CONNECTED successfully!")
                
                # Test the connection by stopping motors (safe state)
                motors[robot_id]['in1'].off()
                motors[robot_id]['in2'].off()
                motors[robot_id]['in3'].off()
                motors[robot_id]['in4'].off()
                
            except Exception as e:
                print(f"  ❌ Failed to connect to {config['name']}: {e}")
                ROBOT_CONFIG[robot_id]['status'] = 'offline'
                motors[robot_id] = None
        else:
            print(f"  ❌ {config['name']} at {ip} is NOT REACHABLE")
            print(f"     Make sure:")
            print(f"     1. Raspberry Pi is powered on")
            print(f"     2. Pi is connected to WiFi")
            print(f"     3. PiGPIO daemon is running on the Pi")
            ROBOT_CONFIG[robot_id]['status'] = 'offline'
            motors[robot_id] = None
    
    print("\n" + "="*60)
    print(f"📊 CONNECTION SUMMARY: {successful_connections}/{len(ROBOT_CONFIG)} robots connected")
    print("="*60 + "\n")
    
    return successful_connections

# ============================================
# MOCK MODE FOR TESTING (NO HARDWARE)
# ============================================

class MockOutputDevice:
    def __init__(self, pin, pin_factory=None):
        self.pin = pin
        self.state = False
    
    def on(self):
        self.state = True
        print(f"  [MOCK] GPIO {self.pin} ON")
    
    def off(self):
        self.state = False
        print(f"  [MOCK] GPIO {self.pin} OFF")

def init_mock_mode():
    """Use mock motors for testing without real Raspberry Pis"""
    global motors
    print("\n" + "="*60)
    print("🎮 RUNNING IN MOCK MODE (No Raspberry Pi hardware)")
    print("="*60)
    
    for robot_id, config in ROBOT_CONFIG.items():
        motors[robot_id] = {
            'in1': MockOutputDevice(config['pins']['in1']),
            'in2': MockOutputDevice(config['pins']['in2']),
            'in3': MockOutputDevice(config['pins']['in3']),
            'in4': MockOutputDevice(config['pins']['in4']),
            'ip': config['ip'],
            'connected': False
        }
        ROBOT_CONFIG[robot_id]['status'] = 'mock'
        print(f"  🎮 {config['name']} - MOCK mode enabled")
    
    print("\n✅ Mock mode initialized for all 10 robots")
    print("="*60 + "\n")

# ============================================
# CONTROL FUNCTIONS
# ============================================

def send_command_to_robot(robot_id, direction):
    """Send movement command to a specific robot"""
    if robot_id not in motors:
        return False
    
    motor = motors[robot_id]
    config = ROBOT_CONFIG[robot_id]
    
    # If motor is None or not connected (and not in mock mode)
    if motor is None:
        print(f"⚠️ {config['name']} is not connected!")
        return False
    
    # Send the appropriate command
    if direction == 'forward':
        motor['in1'].on()
        motor['in2'].off()
        motor['in3'].on()
        motor['in4'].off()
        print(f"  🤖 {config['name']} → FORWARD")
        
    elif direction == 'backward':
        motor['in1'].off()
        motor['in2'].on()
        motor['in3'].off()
        motor['in4'].on()
        print(f"  🤖 {config['name']} → BACKWARD")
        
    elif direction == 'left':
        motor['in1'].off()
        motor['in2'].on()
        motor['in3'].on()
        motor['in4'].off()
        print(f"  🤖 {config['name']} → LEFT TURN")
        
    elif direction == 'right':
        motor['in1'].on()
        motor['in2'].off()
        motor['in3'].off()
        motor['in4'].on()
        print(f"  🤖 {config['name']} → RIGHT TURN")
        
    elif direction == 'stop':
        motor['in1'].off()
        motor['in2'].off()
        motor['in3'].off()
        motor['in4'].off()
        print(f"  🤖 {config['name']} → STOP")
    
    return True

# ============================================
# FLASK ROUTES (WEB ENDPOINTS)
# ============================================

@app.route("/")
def index():
    """Main page - serves the HTML interface"""
    return render_template("index.html")

@app.route("/status")
def get_status():
    """Get connection status of all robots"""
    status = {}
    for robot_id, config in ROBOT_CONFIG.items():
        status[robot_id] = {
            'name': config['name'],
            'ip': config['ip'],
            'status': config['status']
        }
    return jsonify(status)

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Control a specific robot"""
    if robot_id not in ROBOT_CONFIG:
        return jsonify({'error': 'Robot not found'}), 404
    
    if direction not in ['forward', 'backward', 'left', 'right', 'stop']:
        return jsonify({'error': 'Invalid direction'}), 400
    
    # Send command to the robot
    success = send_command_to_robot(robot_id, direction)
    
    if success:
        return jsonify({
            'status': 'ok', 
            'robot': robot_id, 
            'name': ROBOT_CONFIG[robot_id]['name'],
            'direction': direction
        })
    else:
        return jsonify({
            'status': 'error', 
            'robot': robot_id,
            'error': 'Robot not connected'
        }), 503

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    """Control all robots simultaneously"""
    print(f"\n🌐 GLOBAL COMMAND: {direction.upper()} to ALL robots")
    
    results = {}
    for robot_id in ROBOT_CONFIG:
        success = send_command_to_robot(robot_id, direction)
        results[robot_id] = success
    
    return jsonify({
        'status': 'ok',
        'direction': direction,
        'results': results,
        'robots_controlled': len(ROBOT_CONFIG)
    })

@app.route("/speed/<int:robot_id>/<int:speed>")
def set_speed(robot_id, speed):
    """Set speed for a robot (requires PWM hardware)"""
    if robot_id not in ROBOT_CONFIG:
        return jsonify({'error': 'Robot not found'}), 404
    
    # Note: This is a simplified version
    # For real speed control, you'd need to use PWMOutputDevice instead of OutputDevice
    print(f"  ⚙️ {ROBOT_CONFIG[robot_id]['name']} speed set to {speed}/10")
    
    return jsonify({
        'status': 'ok', 
        'robot': robot_id, 
        'speed': speed
    })

@app.route("/reconnect")
def reconnect_robots():
    """Attempt to reconnect to all robots"""
    print("\n🔄 Attempting to reconnect to all robots...")
    count = init_robot_connections()
    return jsonify({'status': 'ok', 'connected': count, 'total': len(ROBOT_CONFIG)})

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("\n" + "🎯" * 30)
    print("🤖 MULTI-ROBOT CONTROL SYSTEM")
    print("   with WiFi Raspberry Pi Support")
    print("🎯" * 30)
    
    # Choose mode based on your setup
    # Option 1: Real hardware (uncomment when Pis are ready)
    # init_robot_connections()
    
    # Option 2: Mock mode for testing (comment out for real hardware)
    init_mock_mode()
    
    print("\n" + "="*60)
    print("🌐 WEB INTERFACE")
    print("="*60)
    print("📡 Server running on:")
    print("   http://localhost:5002")
    print("   http://127.0.0.1:5002")
    print("\n💡 To access from other devices on your network:")
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"   http://{local_ip}:5002")
    print("\n🎮 Control your 10 robots from any browser!")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", debug=True, port=5007)