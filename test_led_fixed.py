from led import Led
import time

print("="*60)
print("LED STRIP TEST")
print("="*60)

LED = Led()

# Try different LED control methods
print("\n1. Trying LED control methods...")

# Method 1: Try color_chase_rainbow_index if it's a list/array
try:
    if hasattr(LED, 'color_chase_rainbow_index'):
        if isinstance(LED.color_chase_rainbow_index, list):
            print("   color_chase_rainbow_index is a list")
            # Try to set color by modifying the list
            pass
        else:
            print("   color_chase_rainbow_index is not callable")
except:
    pass

# Method 2: Try ledIndex (likely works)
print("\n2. Testing ledIndex (set individual LEDs)...")
try:
    # ledIndex(index, r, g, b) - set a single LED
    LED.ledIndex(0, 255, 0, 0)  # First LED red
    print("   ✅ Set LED 0 to RED")
    time.sleep(1)
    LED.ledIndex(0, 0, 255, 0)  # First LED green
    print("   ✅ Set LED 0 to GREEN")
    time.sleep(1)
    LED.ledIndex(0, 0, 0, 255)  # First LED blue
    print("   ✅ Set LED 0 to BLUE")
    time.sleep(1)
    LED.ledIndex(0, 0, 0, 0)    # First LED off
    print("   ✅ Set LED 0 OFF")
except Exception as e:
    print(f"   ❌ ledIndex failed: {e}")

# Method 3: Try color_wipe_index
print("\n3. Testing color_wipe_index...")
try:
    if hasattr(LED, 'color_wipe_index') and callable(LED.color_wipe_index):
        LED.color_wipe_index(0)  # Red wipe
        print("   ✅ color_wipe_index(0) - RED")
        time.sleep(1)
except Exception as e:
    print(f"   ❌ color_wipe_index failed: {e}")

# Method 4: Try rainbowCycle
print("\n4. Testing rainbowCycle...")
try:
    if hasattr(LED, 'rainbowCycle') and callable(LED.rainbowCycle):
        LED.rainbowCycle()
        print("   ✅ rainbowCycle started")
        time.sleep(2)
except Exception as e:
    print(f"   ❌ rainbowCycle failed: {e}")

# Method 5: Try set_color method (common in Freenove)
print("\n5. Testing set_color...")
try:
    if hasattr(LED, 'set_color') and callable(LED.set_color):
        LED.set_color(255, 0, 0)  # Red
        print("   ✅ set_color(255,0,0) - RED")
        time.sleep(1)
        LED.set_color(0, 255, 0)  # Green
        print("   ✅ set_color(0,255,0) - GREEN")
        time.sleep(1)
        LED.set_color(0, 0, 255)  # Blue
        print("   ✅ set_color(0,0,255) - BLUE")
        time.sleep(1)
        LED.set_color(0, 0, 0)    # Off
        print("   ✅ set_color(0,0,0) - OFF")
except Exception as e:
    print(f"   ❌ set_color failed: {e}")

print("\n" + "="*60)
print("LED TEST COMPLETE")
print("If LED didn't light up, check:")
print("   - 5V power connection to LED strip")
print("   - Data pin connection")
print("   - Ground connection")
print("="*60)
