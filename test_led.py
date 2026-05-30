from led import Led
import time

print("="*60)
print("LED STRIP TEST")
print("="*60)

LED = Led()

print("\n1. Testing RED...")
LED.color_chase_rainbow_index(0)
time.sleep(2)

print("\n2. Testing GREEN...")
LED.color_chase_rainbow_index(1)
time.sleep(2)

print("\n3. Testing BLUE...")
LED.color_chase_rainbow_index(2)
time.sleep(2)

print("\n4. Testing RAINBOW...")
LED.rainbowCycle()
time.sleep(3)

print("\n5. Turning OFF...")
LED.ledIndex(0, 0, 0, 0)

print("\n" + "="*60)
print("If LED strip didn't light up, check:")
print("   - 5V power connection")
print("   - Data pin connection")
print("   - Ground connection")
print("="*60)
