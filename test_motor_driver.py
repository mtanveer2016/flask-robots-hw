import RPi.GPIO as GPIO
import time

print("="*60)
print("SIMPLE MOTOR DRIVER TEST")
print("="*60)

# Pin configuration (adjust to your wiring)
IN1 = 13  # Left motor forward
IN2 = 21  # Left motor backward
IN3 = 17  # Right motor forward
IN4 = 27  # Right motor backward

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup pins
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Initialize all to LOW
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

print("\n✅ Pins configured")

def test_sequence():
    print("\n1. Testing FORWARD (both motors)")
    GPIO.output(IN1, GPIO.HIGH)  # Left forward
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)  # Right forward
    GPIO.output(IN4, GPIO.LOW)
    print("   Should move FORWARD")
    time.sleep(2)
    
    print("\n2. Testing BACKWARD (both motors)")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)  # Left backward
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)  # Right backward
    print("   Should move BACKWARD")
    time.sleep(2)
    
    print("\n3. Testing LEFT turn")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)  # Left backward
    GPIO.output(IN3, GPIO.HIGH)  # Right forward
    GPIO.output(IN4, GPIO.LOW)
    print("   Should turn LEFT")
    time.sleep(2)
    
    print("\n4. Testing RIGHT turn")
    GPIO.output(IN1, GPIO.HIGH)  # Left forward
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)  # Right backward
    print("   Should turn RIGHT")
    time.sleep(2)
    
    print("\n5. STOPPING")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("   All motors OFF")

# Run the test
print("\n⚠️  Make sure:")
print("   - Robot is LIFTED off ground")
print("   - Battery connected to motor driver")
print("   - Motor driver has power (LED on)")
print("   - Enable jumpers installed")
print("\n" + "="*60)

input("\nPress ENTER to start motor test...")

try:
    test_sequence()
except KeyboardInterrupt:
    print("\n\nTest interrupted")
finally:
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.cleanup()
    print("\n✅ Test complete")

print("\n" + "="*60)
print("TROUBLESHOOTING")
print("="*60)
print("If motors didn't move:")
print("1. Check motor driver power LED")
print("2. Check battery voltage (need 7.4V-12V)")
print("3. Check enable jumpers on motor driver")
print("4. Check wire connections")
print("5. Test with a multimeter on motor pins")
print("="*60)
