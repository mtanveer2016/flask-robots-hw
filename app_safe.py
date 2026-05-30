from flask import Flask, render_template, request, jsonify
from motor import Ordinary_Car
from buzzer import Buzzer
from led import Led
import threading
import time
import atexit

app = Flask(__name__)

print("\n" + "="*70)
print("🤖 MULTI-ROBOT CONTROL - SAFE VERSION")
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
# MOTOR CONTROL (Using working app's values)
# ============================================

def robot_forward():
    """Move forward"""
    if not emergency_stop_flag:
        PWM.set_motor_model(current_speed, current_speed, current_speed, current_speed)
        print(f"  🔴 FORWARD (speed: {current_speed})")

def robot_backward():
    """Move backward"""
    if not emergency_stop_flag:
        PWM.set_motor_model(-current_speed, -current_speed, -current_speed, -current_speed)
        print(f"  🔴 BACKWARD (speed: {current_speed})")

def robot_left():
    """Turn left"""
    if not emergency_stop_flag:
        PWM.set_motor_model(-current_speed, -current_speed, current_speed, current_speed)
        print(f"  🔴 LEFT TURN")

def robot_right():
    """Turn right"""
    if not emergency_stop_flag:
        PWM.set_motor_model(current_speed, current_speed, -current_speed, -current_speed)
        print(f"  🔴 RIGHT TURN")

def robot_stop():
    """Emergency stop - stops all motors immediately"""
    global emergency_stop_flag, is_dancing
    emergency_stop_flag = True
    is_dancing = False
    PWM.set_motor_model(0, 0, 0, 0)
    print("  🛑 EMERGENCY STOP - All motors stopped")
    # Reset flag after stop
    time.sleep(0.1)
    emergency_stop_flag = False

def beep():
    try:
        buzzer.set_state(True)
        threading.Timer(0.1, lambda: buzzer.set_state(False)).start()
        print("  🔊 BEEP")
    except:
        pass

def led_on():
    try:
        led.ledIndex(0xFF, 255, 255, 255)
        print("  💡 LED ON")
    except:
        pass

def led_off():
    try:
        led.ledIndex(0xFF, 0, 0, 0)
        print("  💡 LED OFF")
    except:
        pass

def led_blink(count=3, delay=0.1):
    """Blink LED for alert"""
    for _ in range(count):
        led_on()
        time.sleep(delay)
        led_off()
        time.sleep(delay)

# ============================================
# SAFE DANCE ROUTINE
# ============================================

def safe_dance_routine():
    """Dance routine with safety checks and stop capability"""
    global is_dancing, emergency_stop_flag
    
    print("\n💃🕺 SAFE DANCE ROUTINE STARTED!")
    led_blink(2, 0.2)
    beep()
    
    # Dance steps with shorter durations for safety
    dance_steps = [
        ('forward', 0.3),
        ('stop', 0.1),
        ('backward', 0.3),
        ('stop', 0.1),
        ('left', 0.2),
        ('stop', 0.1),
        ('right', 0.2),
        ('stop', 0.1),
        ('forward', 0.3),
        ('stop', 0.1),
        ('backward', 0.3),
        ('stop', 0.5),
    ]
    
    for direction, duration in dance_steps:
        if not is_dancing or emergency_stop_flag:
            print("  ⚠️ Dance interrupted!")
            robot_stop()
            break
            
        print(f"  🎵 {direction.upper()} for {duration}s")
        
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
    
    # Ensure robot stops at the end
    robot_stop()
    led_blink(3, 0.1)
    beep()
    is_dancing = False
    print("🎉 DANCE COMPLETE!")

@app.route("/dance")
def start_dance():
    """Start safe dance routine"""
    global is_dancing, dance_thread
    
    if is_dancing:
        return jsonify({'status': 'error', 'message': 'Dance already in progress'})
    
    is_dancing = True
    dance_thread = threading.Thread(target=safe_dance_routine)
    dance_thread.daemon = True
    dance_thread.start()
    
    return jsonify({'status': 'ok', 'message': 'Dance started - press STOP to cancel'})

@app.route("/dance/stop")
def stop_dance():
    """Emergency stop for dance"""
    global is_dancing
    is_dancing = False
    robot_stop()
    print("  🛑 DANCE STOPPED by user")
    return jsonify({'status': 'ok', 'message': 'Dance stopped'})

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
        'speed': current_speed
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Control robot with safety"""
    global is_dancing
    
    # If dancing, stop dance first
    if is_dancing:
        stop_dance()
        time.sleep(0.5)
    
    print(f"\n🤖 Command: {direction.upper()}")
    
    if direction != 'stop':
        beep()
        led_on()
    
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
    
    return jsonify({'status': 'ok', 'direction': direction})

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    return move_robot(0, direction)

@app.route("/stop/all")
def emergency_stop():
    """Emergency stop - stops all movement immediately"""
    global is_dancing
    is_dancing = False
    robot_stop()
    led_off()
    print("\n" + "="*50)
    print("🚨 EMERGENCY STOP ACTIVATED")
    print("="*50)
    return jsonify({'status': 'ok', 'message': 'Emergency stop activated'})

@app.route("/speed/<int:speed>")
def set_speed(speed):
    """Set motor speed (1-4095)"""
    global current_speed
    speed = max(500, min(4000, speed))  # Limit speed range
    current_speed = speed
    print(f"  ⚙️ Speed set to {current_speed}")
    return jsonify({'status': 'ok', 'speed': current_speed})

@app.route("/beep")
def test_beep():
    beep()
    return jsonify({'status': 'ok'})

@app.route("/led/on")
def turn_led_on():
    led_on()
    return jsonify({'status': 'ok'})

@app.route("/led/off")
def turn_led_off():
    led_off()
    return jsonify({'status': 'ok'})

# ============================================
# CLEANUP
# ============================================

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    robot_stop()
    led_off()
    print("✅ Cleanup complete")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 SAFE ROBOT CONTROL SERVER READY")
    print("="*70)
    print(f"📡 Web Interface: http://0.0.0.0:5005")
    print(f"🎮 Speed: {current_speed}")
    print("\n🛡️ SAFETY FEATURES:")
    print("   - Emergency stop: /stop/all")
    print("   - Dance can be stopped with /dance/stop")
    print("   - Any movement command stops dance first")
    print("="*70 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
