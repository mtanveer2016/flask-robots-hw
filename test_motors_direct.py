import lgpio
import time

print("="*60)
print("DIRECT MOTOR TEST - NO FLASK")
print("="*60)

# Open GPIO
handle = lgpio.gpiochip_open(0)
print("✅ GPIO opened")

# Your robot pins (using GPIO22 instead of 17)
pins = {
    'IN1': 13,
    'IN2': 21, 
    'IN3': 22,
    'IN4': 27
}

print(f"\nPin configuration:")
for name, pin in pins.items():
    print(f"  {name} = GPIO{pin}")

# Claim pins
print("\nInitializing pins...")
for name, pin in pins.items():
    try:
        lgpio.gpio_claim_output(handle, pin)
        lgpio.gpio_write(handle, pin, 0)
        print(f"✅ {name} (GPIO{pin}) ready")
    except Exception as e:
        print(f"❌ {name} (GPIO{pin}) failed: {e}")

print("\n" + "="*60)
print("TEST 1: Individual pin test")
print("="*60)

for name, pin in pins.items():
    input(f"\nPress ENTER to test {name} (GPIO{pin})...")
    print(f"  🔴 {name} ON")
    lgpio.gpio_write(handle, pin, 1)
    time.sleep(1)
    print(f"  ⚫ {name} OFF")
    lgpio.gpio_write(handle, pin, 0)

print("\n" + "="*60)
print("TEST 2: FORWARD movement")
print("="*60)
input("\nPress ENTER for FORWARD (2 seconds)...")

# Forward: IN1=ON, IN2=OFF, IN3=ON, IN4=OFF
lgpio.gpio_write(handle, pins['IN1'], 1)
lgpio.gpio_write(handle, pins['IN2'], 0)
lgpio.gpio_write(handle, pins['IN3'], 1)
lgpio.gpio_write(handle, pins['IN4'], 0)
print("🔴 FORWARD - Motors should spin")
time.sleep(2)

# Stop
lgpio.gpio_write(handle, pins['IN1'], 0)
lgpio.gpio_write(handle, pins['IN3'], 0)
print("⚫ STOP")

print("\n" + "="*60)
print("TEST 3: BACKWARD movement")
print("="*60)
input("\nPress ENTER for BACKWARD (2 seconds)...")

# Backward: IN1=OFF, IN2=ON, IN3=OFF, IN4=ON
lgpio.gpio_write(handle, pins['IN1'], 0)
lgpio.gpio_write(handle, pins['IN2'], 1)
lgpio.gpio_write(handle, pins['IN3'], 0)
lgpio.gpio_write(handle, pins['IN4'], 1)
print("🔴 BACKWARD - Motors should spin")
time.sleep(2)

# Stop
lgpio.gpio_write(handle, pins['IN2'], 0)
lgpio.gpio_write(handle, pins['IN4'], 0)
print("⚫ STOP")

print("\n" + "="*60)
print("TEST 4: LEFT turn")
print("="*60)
input("\nPress ENTER for LEFT turn (2 seconds)...")

# Left: IN1=OFF, IN2=ON, IN3=ON, IN4=OFF
lgpio.gpio_write(handle, pins['IN1'], 0)
lgpio.gpio_write(handle, pins['IN2'], 1)
lgpio.gpio_write(handle, pins['IN3'], 1)
lgpio.gpio_write(handle, pins['IN4'], 0)
print("🔴 LEFT - Robot should turn left")
time.sleep(2)

# Stop
lgpio.gpio_write(handle, pins['IN2'], 0)
lgpio.gpio_write(handle, pins['IN3'], 0)
print("⚫ STOP")

print("\n" + "="*60)
print("TEST 5: RIGHT turn")
print("="*60)
input("\nPress ENTER for RIGHT turn (2 seconds)...")

# Right: IN1=ON, IN2=OFF, IN3=OFF, IN4=ON
lgpio.gpio_write(handle, pins['IN1'], 1)
lgpio.gpio_write(handle, pins['IN2'], 0)
lgpio.gpio_write(handle, pins['IN3'], 0)
lgpio.gpio_write(handle, pins['IN4'], 1)
print("🔴 RIGHT - Robot should turn right")
time.sleep(2)

# Stop
lgpio.gpio_write(handle, pins['IN1'], 0)
lgpio.gpio_write(handle, pins['IN4'], 0)
print("⚫ STOP")

# Cleanup
print("\n🧹 Cleaning up...")
for pin in pins.values():
    try:
        lgpio.gpio_free(handle, pin)
    except:
        pass

lgpio.gpiochip_close(handle)
print("✅ Test complete")

print("\n" + "="*60)
print("TROUBLESHOOTING")
print("="*60)
print("If motors didn't move:")
print("1. Check motor driver power LED - is it ON?")
print("2. Check battery voltage (needs 7.4V-12V)")
print("3. Check ENA/ENB jumpers on motor driver")
print("4. Check wire connections:")
print("   - GPIO13 (Pin33) → IN1")
print("   - GPIO21 (Pin40) → IN2")
print("   - GPIO22 (Pin15) → IN3 (using 22, not 17!)")
print("   - GPIO27 (Pin13) → IN4")
print("   - GND → Motor driver GND")
print("5. Check common ground between Pi and motor driver")
print("="*60)
