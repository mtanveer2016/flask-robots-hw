#!/usr/bin/env python3
import lgpio
import time

print("="*60)
print("MOTOR TEST USING LGPIO DIRECTLY")
print("="*60)

# Open GPIO chip
handle = lgpio.gpiochip_open(0)
print(f"✅ GPIO chip opened (handle: {handle})")

# Motor pins
IN1, IN2, IN3, IN4 = 13, 21, 17, 27

# Claim pins as outputs
print("Claiming GPIO pins...")
for pin in [IN1, IN2, IN3, IN4]:
    try:
        lgpio.gpio_claim_output(handle, pin)
        print(f"   ✅ GPIO {pin} claimed as output")
    except Exception as e:
        print(f"   ❌ GPIO {pin} failed: {e}")

# Initialize all pins to LOW
for pin in [IN1, IN2, IN3, IN4]:
    lgpio.gpio_write(handle, pin, 0)

print("\n⚠️  Lift robot off ground!")
input("\nPress ENTER to test FORWARD...")

print("\n>>> FORWARD <<<")
lgpio.gpio_write(handle, IN1, 1)  # Left forward ON
lgpio.gpio_write(handle, IN2, 0)  # Left backward OFF
lgpio.gpio_write(handle, IN3, 1)  # Right forward ON
lgpio.gpio_write(handle, IN4, 0)  # Right backward OFF
print("   Motors should spin FORWARD")
time.sleep(2)

print("\n>>> STOP <<<")
lgpio.gpio_write(handle, IN1, 0)
lgpio.gpio_write(handle, IN3, 0)
print("   Motors should stop")
time.sleep(1)

input("\nPress ENTER to test BACKWARD...")

print("\n>>> BACKWARD <<<")
lgpio.gpio_write(handle, IN1, 0)
lgpio.gpio_write(handle, IN2, 1)  # Left backward ON
lgpio.gpio_write(handle, IN3, 0)
lgpio.gpio_write(handle, IN4, 1)  # Right backward ON
print("   Motors should spin BACKWARD")
time.sleep(2)

print("\n>>> STOP <<<")
lgpio.gpio_write(handle, IN2, 0)
lgpio.gpio_write(handle, IN4, 0)
print("   Motors should stop")

input("\nPress ENTER to test LEFT TURN...")

print("\n>>> LEFT TURN <<<")
lgpio.gpio_write(handle, IN1, 0)
lgpio.gpio_write(handle, IN2, 1)  # Left backward
lgpio.gpio_write(handle, IN3, 1)  # Right forward
lgpio.gpio_write(handle, IN4, 0)
print("   Robot should turn LEFT")
time.sleep(2)

print("\n>>> STOP <<<")
lgpio.gpio_write(handle, IN2, 0)
lgpio.gpio_write(handle, IN3, 0)

input("\nPress ENTER to test RIGHT TURN...")

print("\n>>> RIGHT TURN <<<")
lgpio.gpio_write(handle, IN1, 1)  # Left forward
lgpio.gpio_write(handle, IN2, 0)
lgpio.gpio_write(handle, IN3, 0)
lgpio.gpio_write(handle, IN4, 1)  # Right backward
print("   Robot should turn RIGHT")
time.sleep(2)

print("\n>>> STOP <<<")
lgpio.gpio_write(handle, IN1, 0)
lgpio.gpio_write(handle, IN4, 0)

# Cleanup
print("\nCleaning up...")
for pin in [IN1, IN2, IN3, IN4]:
    lgpio.gpio_write(handle, pin, 0)
    lgpio.gpio_free(handle, pin)

lgpio.gpiochip_close(handle)

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nIf wheels still don't spin, check:")
print("1. Motor driver power LED")
print("2. Battery voltage (7.4V-12V)")
print("3. Enable jumpers on motor driver")
print("4. Wire connections")
print("="*60)
