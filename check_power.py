import RPi.GPIO as GPIO
import time

print("="*60)
print("HARDWARE POWER CHECK")
print("="*60)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor driver enable pins (common on L298N/L293D)
# Check if your motor driver has enable pins
ENABLE_PINS = [12, 13, 18]  # Try common enable pins

for pin in ENABLE_PINS:
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        print(f"✅ Set GPIO {pin} HIGH (enable signal)")
    except:
        pass

print("\n⚠️  CHECK THESE PHYSICAL THINGS:")
print("1. Does your motor driver board have a power LED? Is it ON?")
print("2. Is the battery connected to the motor driver (not just the Pi)?")
print("3. Are the motor wires connected securely?")
print("4. Does your motor driver have enable jumpers? Are they installed?")

GPIO.cleanup()
