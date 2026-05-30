from flask import Flask, render_template, request, jsonify
from motor import Ordinary_Car
from buzzer import Buzzer
from led import Led
import threading
import time
import atexit

app = Flask(__name__)

print("\n" + "="*70)
print("🤖 MULTI-ROBOT CONTROL - COLOR LED FEEDBACK")
print("="*70)

# Initialize hardware
PWM = Ordinary_Car()
buzzer = Buzzer()
led = Led()

print("✅ Hardware initialized")

# ============================================
# SAFETY VARIABLES
# ============================================
is_dancing = False
dance_thread = None
emergency_stop_flag = False
current_speed = 2000

# ============================================
# COLOR DEFINITIONS (RGB values)
# ============================================
# Each movement has its own unique color
COLORS = {
    'forward': (0, 255, 0),      # GREEN - Go forward
    'backward': (255, 0, 0),     # RED - Stop/Reverse
    'left': (255, 255, 0),       # YELLOW - Turn left
    'right': (0, 255, 255),      # CYAN - Turn right
    'stop': (0, 0, 0),           # OFF
    'dance_start': (255, 0, 255), # MAGENTA - Dance mode
    'dance_step': (255, 255, 255), # WHITE - Dance step
    'emergency': (255, 0, 0),    # RED FLASH - Emergency
}

def set_led_color(r, g, b):
    """Set LED to specific RGB color"""
    try:
        led.ledIndex(0xFF, r, g, b)
        print(f"  💡 LED: RGB({r},{g},{b})")
    except Exception as e:
        print(f"  ⚠️ LED error: {e}")

def led_forward():
    """Green - Moving forward"""
    set_led_color(*COLORS['forward'])

def led_backward():
    """Red - Moving backward"""
    set_led_color(*COLORS['backward'])

def led_left():
    """Yellow - Turning left"""
    set_led_color(*COLORS['left'])

def led_right():
    """Cyan - Turning right"""
    set_led_color(*COLORS['right'])

def led_stop():
    """Off - Stopped"""
    set_led_color(*COLORS['stop'])

def led_dance_start():
    """Magenta - Dance starting"""
    set_led_color(*COLORS['dance_start'])

def led_dance_step():
    """White - Dance step"""
    set_led_color(*COLORS['dance_step'])

def led_emergency():
    """Red flash - Emergency"""
    for _ in range(3):
        set_led_color(*COLORS['emergency'])
        time.sleep(0.1)
        led_stop()
        time.sleep(0.1)

def led_blink_color(color_rgb, count=3, delay=0.15):
    """Blink LED with specific color"""
    for _ in range(count):
        set_led_color(*color_rgb)
        time.sleep(delay)
        led_stop()
        time.sleep(delay)

def beep():
    try:
        buzzer.set_state(True)
        threading.Timer(0.1, lambda: buzzer.set_state(False)).start()
        print("  🔊 BEEP")
    except:
        pass

# ============================================
# MOTOR CONTROL WITH COLOR FEEDBACK
# ============================================

def robot_forward():
    """Move forward with GREEN LED"""
    if not emergency_stop_flag:
        PWM.set_motor_model(-current_speed, -current_speed, -current_speed, -current_speed)
        led_forward()
        print(f"  🔴 FORWARD (speed: {current_speed}) - 🟢 GREEN LED")

def robot_backward():
    """Move backward with RED LED"""
    if not emergency_stop_flag:
        PWM.set_motor_model(current_speed, current_speed, current_speed, current_speed)
        led_backward()
        print(f"  🔴 BACKWARD (speed: {current_speed}) - 🔴 RED LED")

def robot_left():
    """Turn left with YELLOW LED"""
    if not emergency_stop_flag:
        PWM.set_motor_model(current_speed, current_speed, -current_speed, -current_speed)
        led_left()
        print(f"  🔴 LEFT TURN - 🟡 YELLOW LED")

def robot_right():
    """Turn right with CYAN LED"""
    if not emergency_stop_flag:
        PWM.set_motor_model(-current_speed, -current_speed, current_speed, current_speed)
        led_right()
        print(f"  🔴 RIGHT TURN - 🔵 CYAN LED")

def robot_stop():
    """Stop with LED OFF"""
    global emergency_stop_flag, is_dancing
    emergency_stop_flag = True
    is_dancing = False
    PWM.set_motor_model(0, 0, 0, 0)
    led_stop()
    print("  🛑 EMERGENCY STOP - All motors stopped - 💡 LED OFF")
    time.sleep(0.1)
    emergency_stop_flag = False

# ============================================
# SAFE DANCE ROUTINE WITH COLOR CHANGES
# ============================================

def safe_dance_routine():
    """Dance routine with color-changing LED effects"""
    global is_dancing, emergency_stop_flag
    
    print("\n💃🕺 COLOR DANCE ROUTINE STARTED!")
    
    # Dance start effect - Magenta blinking
    led_dance_start()
    beep()
    time.sleep(0.3)
    led_stop()
    time.sleep(0.2)
    led_dance_start()
    time.sleep(0.3)
    led_stop()
    
    # Dance steps with colors
    dance_steps = [
        ('forward', 0.3, COLORS['forward']),    # Green
        ('stop', 0.1, COLORS['stop']),
        ('backward', 0.3, COLORS['backward']),  # Red
        ('stop', 0.1, COLORS['stop']),
        ('left', 0.2, COLORS['left']),          # Yellow
        ('stop', 0.1, COLORS['stop']),
        ('right', 0.2, COLORS['right']),        # Cyan
        ('stop', 0.1, COLORS['stop']),
        ('forward', 0.3, COLORS['forward']),    # Green
        ('stop', 0.1, COLORS['stop']),
        ('backward', 0.3, COLORS['backward']),  # Red
        ('stop', 0.5, COLORS['stop']),
    ]
    
    for direction, duration, color in dance_steps:
        if not is_dancing or emergency_stop_flag:
            print("  ⚠️ Dance interrupted!")
            robot_stop()
            break
        
        # Set LED color for this step
        set_led_color(*color)
        print(f"  🎵 {direction.upper()} for {duration}s - LED: {color}")
        
        if direction == 'forward':
            PWM.set_motor_model(current_speed, current_speed, current_speed, current_speed)
        elif direction == 'backward':
            PWM.set_motor_model(-current_speed, -current_speed, -current_speed, -current_speed)
        elif direction == 'left':
            PWM.set_motor_model(-current_speed, -current_speed, current_speed, current_speed)
        elif direction == 'right':
            PWM.set_motor_model(current_speed, current_speed, -current_speed, -current_speed)
        elif direction == 'stop':
            PWM.set_motor_model(0, 0, 0, 0)
        
        time.sleep(duration)
    
    # Dance end effect - Rainbow flash
    for color in [COLORS['forward'], COLORS['backward'], COLORS['left'], COLORS['right'], COLORS['dance_start']]:
        set_led_color(*color)
        time.sleep(0.1)
    
    robot_stop()
    beep()
    is_dancing = False
    print("🎉 DANCE COMPLETE! 🎉")

# ============================================
# FLASK ROUTES
# ============================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify({
        'status': 'ok',
        'is_dancing': is_dancing,
        'speed': current_speed,
        'colors': COLORS
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Control robot with color feedback"""
    global is_dancing
    
    if is_dancing:
        stop_dance()
        time.sleep(0.5)
    
    print(f"\n🤖 Command: {direction.upper()}")
    
    if direction != 'stop':
        beep()
    
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
    
    return jsonify({'status': 'ok', 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    return move_robot(0, direction)

@app.route("/stop/all")
def emergency_stop():
    """Emergency stop with RED flashing LED"""
    global is_dancing
    is_dancing = False
    robot_stop()
    led_emergency()
    beep()
    print("\n" + "="*50)
    print("🚨 EMERGENCY STOP ACTIVATED - RED FLASH")
    print("="*50)
    return jsonify({'status': 'ok', 'message': 'Emergency stop activated'})

@app.route("/dance")
def start_dance():
    """Start color dance routine"""
    global is_dancing, dance_thread
    
    if is_dancing:
        return jsonify({'status': 'error', 'message': 'Dance already in progress'})
    
    is_dancing = True
    dance_thread = threading.Thread(target=safe_dance_routine)
    dance_thread.daemon = True
    dance_thread.start()
    
    return jsonify({'status': 'ok', 'message': 'Color dance started!'})

@app.route("/dance/stop")
def stop_dance():
    """Stop dance routine"""
    global is_dancing
    is_dancing = False
    robot_stop()
    print("  🛑 DANCE STOPPED")
    return jsonify({'status': 'ok', 'message': 'Dance stopped'})

@app.route("/speed/<int:speed>")
def set_speed(speed):
    """Set motor speed (500-4000)"""
    global current_speed
    speed = max(500, min(4000, speed))
    current_speed = speed
    # Blink LED to confirm speed change
    led_blink_color(COLORS['dance_step'], 2, 0.1)
    print(f"  ⚙️ Speed set to {current_speed}")
    return jsonify({'status': 'ok', 'speed': current_speed})

@app.route("/led/test")
def led_test():
    """Test all LED colors"""
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
        set_led_color(*color)
        time.sleep(0.5)
    
    led_stop()
    return jsonify({'status': 'ok', 'message': 'LED test complete'})

@app.route("/beep")
def test_beep():
    beep()
    return jsonify({'status': 'ok'})

# ============================================
# CLEANUP
# ============================================

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    robot_stop()
    led_stop()
    print("✅ Cleanup complete")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎨 COLOR LED ROBOT CONTROL SERVER READY")
    print("="*70)
    print(f"📡 Web Interface: http://0.0.0.0:5005")
    print(f"🎮 Speed: {current_speed}")
    print("\n🎨 LED COLOR GUIDE:")
    print("   🟢 GREEN  = Moving FORWARD")
    print("   🔴 RED    = Moving BACKWARD")
    print("   🟡 YELLOW = Turning LEFT")
    print("   🔵 CYAN   = Turning RIGHT")
    print("   ⚫ OFF    = STOPPED")
    print("   🟣 MAGENTA = DANCE mode")
    print("   🔴 FLASH  = EMERGENCY")
    print("\n🛡️ SAFETY FEATURES:")
    print("   - Emergency stop: /stop/all")
    print("   - Dance can be stopped with /dance/stop")
    print("   - Test LED colors: /led/test")
    print("="*70 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
