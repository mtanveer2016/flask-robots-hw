from flask import Flask, render_template, request, jsonify
from motor import Ordinary_Car
from buzzer import Buzzer
from led import Led
import requests
import threading
import time
import atexit

app = Flask(__name__)

print("\n" + "="*70)
print("🤖 MULTI-ROBOT CONTROL - COLOR LED FEEDBACK")
print("="*70)

# ============================================
# LOCAL HARDWARE (Robot 1)
# ============================================
PWM = Ordinary_Car()
buzzer = Buzzer()
led = Led()

print("✅ Local hardware (Robot 1) initialized")

# ============================================
# ROBOT CONFIGURATION
# ============================================
# Add each robot's IP address here
# For Robot 1 (local), use 'localhost'
# For other robots, use their IP addresses
ROBOTS = {
    0: {
        'name': 'Robot 1',
        'ip': 'localhost',
        'port': 5005,
        'local': True,
        'active': True
    },
    # Add Robot 2 when ready (uncomment and set correct IP)
    # 1: {
    #     'name': 'Robot 2',
    #     'ip': '192.168.1.102',
    #     'port': 5005,
    #     'local': False,
    #     'active': True
    # },
    # 2: {
    #     'name': 'Robot 3',
    #     'ip': '192.168.1.103',
    #     'port': 5005,
    #     'local': False,
    #     'active': True
    # },
}

# ============================================
# COLOR DEFINITIONS (RGB values)
# ============================================
COLORS = {
    'forward': (0, 255, 0),      # GREEN - Go forward
    'backward': (255, 0, 0),     # RED - Stop/Reverse
    'left': (255, 255, 0),       # YELLOW - Turn left
    'right': (0, 255, 255),      # CYAN - Turn right
    'stop': (0, 0, 0),           # OFF
    'dance_start': (255, 0, 255), # MAGENTA - Dance mode
    'dance_step': (255, 255, 255), # WHITE - Dance step
    'emergency': (255, 0, 0),    # RED FLASH
}

def set_local_led_color(r, g, b):
    """Set local robot LED color"""
    try:
        led.ledIndex(0xFF, r, g, b)
        print(f"  💡 LED: RGB({r},{g},{b})")
    except Exception as e:
        print(f"  ⚠️ LED error: {e}")

def led_local_forward():
    set_local_led_color(*COLORS['forward'])

def led_local_backward():
    set_local_led_color(*COLORS['backward'])

def led_local_left():
    set_local_led_color(*COLORS['left'])

def led_local_right():
    set_local_led_color(*COLORS['right'])

def led_local_stop():
    set_local_led_color(*COLORS['stop'])

def led_local_dance():
    set_local_led_color(*COLORS['dance_start'])

def led_local_emergency():
    for _ in range(3):
        set_local_led_color(*COLORS['emergency'])
        time.sleep(0.1)
        led_local_stop()
        time.sleep(0.1)

def beep_local():
    try:
        buzzer.set_state(True)
        threading.Timer(0.1, lambda: buzzer.set_state(False)).start()
        print("  🔊 BEEP")
    except:
        pass

# ============================================
# MOTOR CONTROL FOR LOCAL ROBOT (Robot 1)
# ============================================
SPEED = 2000

def local_forward():
    PWM.set_motor_model(-SPEED, -SPEED, -SPEED, -SPEED)
    led_local_forward()
    beep_local()
    print("  🔴 FORWARD - 🟢 GREEN LED")

def local_backward():
    PWM.set_motor_model(SPEED, SPEED, SPEED, SPEED)
    led_local_backward()
    beep_local()
    print("  🔴 BACKWARD - 🔴 RED LED")

def local_left():
    PWM.set_motor_model(-SPEED, -SPEED, SPEED, SPEED)
    led_local_left()
    beep_local()
    print("  🔴 LEFT TURN - 🟡 YELLOW LED")

def local_right():
    PWM.set_motor_model(SPEED, SPEED, -SPEED, -SPEED)
    led_local_right()
    beep_local()
    print("  🔴 RIGHT TURN - 🔵 CYAN LED")

def local_stop():
    PWM.set_motor_model(0, 0, 0, 0)
    led_local_stop()
    print("  ⚫ STOPPED - 💡 LED OFF")

# ============================================
# REMOTE ROBOT CONTROL
# ============================================
def send_to_remote_robot(robot_id, direction):
    """Send command to remote robot"""
    robot = ROBOTS[robot_id]
    url = f"http://{robot['ip']}:{robot['port']}/move/{direction}"
    try:
        response = requests.get(url, timeout=1)
        print(f"  ✅ {robot['name']}: {direction}")
        return True
    except Exception as e:
        print(f"  ❌ {robot['name']}: Failed - {e}")
        return False

# ============================================
# MAIN ROUTING FUNCTION
# ============================================
def control_robot(robot_id, direction):
    """Route command to correct robot"""
    if robot_id not in ROBOTS:
        return False
    
    robot = ROBOTS[robot_id]
    
    if robot['local']:
        # Control local robot
        if direction == 'forward':
            local_forward()
        elif direction == 'backward':
            local_backward()
        elif direction == 'left':
            local_left()
        elif direction == 'right':
            local_right()
        elif direction == 'stop':
            local_stop()
        return True
    else:
        # Control remote robot
        return send_to_remote_robot(robot_id, direction)

# ============================================
# FLASK ROUTES
# ============================================

@app.route("/")
def index():
    """Main interface - your beautiful HTML with all robot cards"""
    return render_template("index.html")

@app.route("/status")
def status():
    """Get status of all robots"""
    robot_status = {}
    for robot_id, robot in ROBOTS.items():
        robot_status[robot_id] = {
            'name': robot['name'],
            'ip': robot['ip'],
            'local': robot['local'],
            'active': robot['active']
        }
    return jsonify({
        'status': 'ok',
        'robots': robot_status,
        'total': len(ROBOTS),
        'colors': COLORS
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Control a specific robot with color feedback"""
    if robot_id not in ROBOTS:
        return jsonify({'error': 'Robot not found'}), 404
    
    print(f"\n🤖 {ROBOTS[robot_id]['name']}: {direction.upper()}")
    
    success = control_robot(robot_id, direction)
    
    return jsonify({
        'status': 'ok' if success else 'error',
        'robot': robot_id,
        'direction': direction
    })

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    """Control ALL robots simultaneously"""
    print(f"\n🌐 ALL ROBOTS: {direction.upper()}")
    
    # LED feedback on local robot for global command
    if direction != 'stop':
        led_local_dance()
        beep_local()
    else:
        led_local_stop()
    
    results = {}
    for robot_id in ROBOTS:
        results[robot_id] = control_robot(robot_id, direction)
    
    return jsonify({
        'status': 'ok',
        'direction': direction,
        'results': results
    })

@app.route("/dance")
def dance():
    """Synchronized dance routine for all robots with color effects"""
    print("\n💃🕺 SYNC DANCE WITH ALL ROBOTS!")
    
    # Dance start effect - Magenta blinking
    led_local_dance()
    beep_local()
    time.sleep(0.3)
    led_local_stop()
    time.sleep(0.2)
    led_local_dance()
    time.sleep(0.3)
    led_local_stop()
    
    dance_steps = [
        ('forward', 0.4, COLORS['forward']),
        ('backward', 0.4, COLORS['backward']),
        ('left', 0.3, COLORS['left']),
        ('right', 0.3, COLORS['right']),
        ('forward', 0.3, COLORS['forward']),
        ('backward', 0.3, COLORS['backward']),
        ('stop', 0.2, COLORS['stop']),
    ]
    
    def execute_dance():
        for direction, duration, color in dance_steps:
            print(f"  🎵 {direction.upper()} - Color: {color}")
            # Show color on local LED
            set_local_led_color(*color)
            # Send to all robots
            for robot_id in ROBOTS:
                control_robot(robot_id, direction)
            time.sleep(duration)
        # Final stop
        for robot_id in ROBOTS:
            control_robot(robot_id, 'stop')
        led_local_stop()
        print("🎉 DANCE COMPLETE!")
    
    # Run dance in background thread
    dance_thread = threading.Thread(target=execute_dance)
    dance_thread.start()
    
    return jsonify({'status': 'ok', 'message': 'Color dance started!'})

@app.route("/dance/stop")
def stop_dance():
    """Stop dance immediately"""
    print("\n🛑 DANCE STOPPED!")
    for robot_id in ROBOTS:
        control_robot(robot_id, 'stop')
    led_local_stop()
    return jsonify({'status': 'ok', 'message': 'Dance stopped'})

@app.route("/emergency/stop")
def emergency_stop():
    """Emergency stop all robots with flashing red LED"""
    print("\n🚨 EMERGENCY STOP ALL ROBOTS!")
    
    # Flashing red LED for emergency
    for _ in range(3):
        set_local_led_color(*COLORS['emergency'])
        time.sleep(0.1)
        led_local_stop()
        time.sleep(0.1)
    
    for robot_id in ROBOTS:
        control_robot(robot_id, 'stop')
    
    beep_local()
    return jsonify({'status': 'ok', 'message': 'Emergency stop activated'})

@app.route("/led/test")
def led_test():
    """Test all LED colors on local robot"""
    print("\n🎨 LED COLOR TEST")
    colors_to_test = [
        ('FORWARD', COLORS['forward']),
        ('BACKWARD', COLORS['backward']),
        ('LEFT', COLORS['left']),
        ('RIGHT', COLORS['right']),
        ('DANCE', COLORS['dance_start']),
    ]
    
    for name, color in colors_to_test:
        print(f"  Testing {name}: {color}")
        set_local_led_color(*color)
        time.sleep(0.5)
    
    led_local_stop()
    return jsonify({'status': 'ok', 'message': 'LED test complete'})

@app.route("/speed/<int:speed>")
def set_speed(speed):
    """Set motor speed for local robot"""
    global SPEED
    SPEED = max(500, min(4000, speed))
    print(f"  ⚙️ Speed set to {SPEED}")
    return jsonify({'status': 'ok', 'speed': SPEED})

# ============================================
# CLEANUP
# ============================================

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    local_stop()
    print("✅ Cleanup complete")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎨 MULTI-ROBOT CONTROL WITH COLOR LED FEEDBACK")
    print("="*70)
    print(f"📡 Web Interface: http://0.0.0.0:5005")
    print(f"🤖 Configured Robots: {len(ROBOTS)}")
    print("\n🎨 LED COLOR GUIDE:")
    print("   🟢 GREEN  = Moving FORWARD")
    print("   🔴 RED    = Moving BACKWARD")
    print("   🟡 YELLOW = Turning LEFT")
    print("   🔵 CYAN   = Turning RIGHT")
    print("   ⚫ OFF    = STOPPED")
    print("   🟣 MAGENTA = DANCE mode")
    print("   🔴 FLASH  = EMERGENCY")
    print("\n🎮 Available Commands:")
    print("   - /move/0/forward  - Robot 1 forward")
    print("   - /move/all/forward - ALL robots forward")
    print("   - /dance           - Synchronized dance")
    print("   - /emergency/stop  - Stop all robots")
    print("   - /led/test        - Test LED colors")
    print("="*70 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
