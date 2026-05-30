import RPi.GPIO as GPIO
import time

print("="*60)
print("DIRECT GPIO PIN TEST")
print("="*60)
print("This tests if your Pi can actually control the pins")
print("You should hear clicks or see LED flashes if connected\n")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Your motor control pins
MOTOR_PINS = [13, 21, 17, 27]

# Setup all pins
for pin in MOTOR_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    print(f"✓ GPIO {pin} set as output")

print("\nTesting each pin one by one...")
print("Listen for clicks or use a multimeter to check voltage\n")

for pin in MOTOR_PINS:
    print(f"Testing GPIO {pin}...")
    GPIO.output(pin, GPIO.HIGH)
    print(f"  GPIO {pin} = HIGH (3.3V)")
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    print(f"  GPIO {pin} = LOW (0V)")
    time.sleep(0.5)

print("\n✅ GPIO test complete")
GPIO.cleanup()

print("\n📊 EXPECTED VOLTAGES:")
print("   Between GPIO pin and GND:")
print("   HIGH should read ~3.3V")
print("   LOW should read ~0V")
print("\nIf you see these voltages, your Pi is working correctly.")
print("If not, check your Pi's GPIO header connection.")
