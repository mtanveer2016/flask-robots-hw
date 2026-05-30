import RPi.GPIO as GPIO
import time
from motor import Ordinary_Car

print("="*60)
print("ENABLE PIN CHECK")
print("="*60)

# Some motor drivers have enable pins on GPIO 12, 18, etc.
enable_pins = [12, 18, 22, 23]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("\nChecking for enable pins...")
for pin in enable_pins:
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        print(f"✅ Set GPIO{pin} HIGH (enable signal)")
    except:
        pass

PWM = Ordinary_Car()

input("\nPress ENTER to test FORWARD with enables ON...")
print("🔴 FORWARD")
PWM.set_motor_model(1, 0, 1, 0)
time.sleep(2)
PWM.set_motor_model(0, 0, 0, 0)
print("⚫ STOP")

GPIO.cleanup()

print("\n" + "="*60)
print("If robot moved: Enable pins were the issue")
print("Install jumpers on ENA/ENB or set GPIO high")
print("="*60)
