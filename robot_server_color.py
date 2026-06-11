from flask import Flask, request, jsonify
from motor import Ordinary_Car
from led import Led
import atexit

app = Flask(__name__)
PWM = Ordinary_Car()
led = Led()
SPEED = 2000

# Colors
COLORS = {
    'forward': (0, 255, 0),
    'backward': (255, 0, 0),
    'left': (255, 255, 0),
    'right': (0, 255, 255),
    'stop': (0, 0, 0),
}

def set_led_color(r, g, b):
    try:
        led.ledIndex(0xFF, r, g, b)
    except:
        pass

@app.route("/move/<direction>")
def move(direction):
    if direction == 'forward':
        PWM.set_motor_model(SPEED, SPEED, SPEED, SPEED)
        set_led_color(*COLORS['forward'])
    elif direction == 'backward':
        PWM.set_motor_model(-SPEED, -SPEED, -SPEED, -SPEED)
        set_led_color(*COLORS['backward'])
    elif direction == 'left':
        PWM.set_motor_model(-SPEED, -SPEED, SPEED, SPEED)
        set_led_color(*COLORS['left'])
    elif direction == 'right':
        PWM.set_motor_model(SPEED, SPEED, -SPEED, -SPEED)
        set_led_color(*COLORS['right'])
    elif direction == 'stop':
        PWM.set_motor_model(0, 0, 0, 0)
        set_led_color(*COLORS['stop'])
    return jsonify({'status': 'ok'})

@atexit.register
def cleanup():
    PWM.set_motor_model(0, 0, 0, 0)
    set_led_color(0, 0, 0)

if __name__ == "__main__":
    print("🤖 Robot Server with Color LED Ready")
    app.run(host="0.0.0.0", port=5005)
