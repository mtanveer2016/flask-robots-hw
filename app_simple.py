from flask import Flask, render_template, request, jsonify
import atexit

app = Flask(__name__)

print("\n" + "="*60)
print("🤖 ROBOT CONTROL - SIMPLE VERSION")
print("="*60)

# Import motor
from motor import Ordinary_Car

# Import LED (with error handling)
try:
    from led_pi5_fix import Led
    led_available = True
    print("✅ LED module loaded")
except Exception as e:
    print(f"⚠️ LED not available: {e}")
    led_available = False
    Led = None

PWM = Ordinary_Car()
print("✅ Motor initialized")

if led_available:
    LED = Led()
    print("✅ LED initialized")
else:
    LED = None

print("="*60 + "\n")

def robot_forward():
    PWM.set_motor_model(1, 0, 1, 0)
    print("  🔴 FORWARD")

def robot_backward():
    PWM.set_motor_model(0, 1, 0, 1)
    print("  🔴 BACKWARD")

def robot_left():
    PWM.set_motor_model(0, 1, 1, 0)
    print("  🔴 LEFT")

def robot_right():
    PWM.set_motor_model(1, 0, 0, 1)
    print("  🔴 RIGHT")

def robot_stop():
    PWM.set_motor_model(0, 0, 0, 0)
    print("  ⚫ STOP")

def led_green():
    if LED:
        try:
            LED.ledIndex(0xFF, 0, 255, 0)
            print("  🟢 LED GREEN")
        except:
            pass

def led_off():
    if LED:
        try:
            LED.ledIndex(0xFF, 0, 0, 0)
            print("  ⚫ LED OFF")
        except:
            pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    print(f"\n🤖 Robot: {direction.upper()}")
    
    if direction != 'stop':
        led_green()
    
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
    
    return jsonify({'status': 'ok'})

@atexit.register
def cleanup():
    print("\n🧹 Cleaning up...")
    robot_stop()
    if LED:
        led_off()

if __name__ == "__main__":
    print("🚀 Server: http://10.243.53.235:5005")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", debug=False, port=5005)
