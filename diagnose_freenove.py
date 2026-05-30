#!/usr/bin/env python3
from motor import Ordinary_Car
import time
import sys

print("="*70)
print("FREENOVE ROBOT DIAGNOSTIC")
print("="*70)

# Initialize
PWM = Ordinary_Car()
print("\n✅ Motor controller initialized")

# Check if we can control PWM (for speed)
try:
    # Try to set PWM if available
    if hasattr(PWM, 'pwm'):
        print(f"   PWM type: {type(PWM.pwm)}")
        if hasattr(PWM.pwm, 'set_pwm_freq'):
            PWM.pwm.set_pwm_freq(100)
            print("   ✅ PWM frequency set")
except Exception as e:
    print(f"   ⚠️ PWM control: {e}")

print("\n" + "="*70)
print("TEST 1: Individual Motor Test (Lift robot off ground!)")
print("="*70)

input("\nPress ENTER to test LEFT MOTOR ONLY...")

print("   Left motor FORWARD (should spin)")
PWM.set_motor_model(1, 0, 0, 0)
time.sleep(2)
print("   Stopping...")
PWM.set_motor_model(0, 0, 0, 0)
time.sleep(1)

print("\n   Left motor BACKWARD (should spin opposite)")
PWM.set_motor_model(0, 1, 0, 0)
time.sleep(2)
print("   Stopping...")
PWM.set_motor_model(0, 0, 0, 0)
time.sleep(1)

input("\nPress ENTER to test RIGHT MOTOR ONLY...")

print("   Right motor FORWARD (should spin)")
PWM.set_motor_model(0, 0, 1, 0)
time.sleep(2)
print("   Stopping...")
PWM.set_motor_model(0, 0, 0, 0)
time.sleep(1)

print("\n   Right motor BACKWARD (should spin opposite)")
PWM.set_motor_model(0, 0, 0, 1)
time.sleep(2)
print("   Stopping...")
PWM.set_motor_model(0, 0, 0, 0)
time.sleep(1)

print("\n" + "="*70)
print("TEST 2: Both Motors Together")
print("="*70)

input("\nPress ENTER for FORWARD...")
PWM.set_motor_model(1, 0, 1, 0)
time.sleep(3)
print("   Stopping...")
PWM.set_motor_model(0, 0, 0, 0)

input("\nPress ENTER for BACKWARD...")
PWM.set_motor_model(0, 1, 0, 1)
time.sleep(3)
print("   Stopping...")
PWM.set_motor_model(0, 0, 0, 0)

input("\nPress ENTER for LEFT TURN...")
PWM.set_motor_model(0, 1, 1, 0)
time.sleep(2)
PWM.set_motor_model(0, 0, 0, 0)

input("\nPress ENTER for RIGHT TURN...")
PWM.set_motor_model(1, 0, 0, 1)
time.sleep(2)
PWM.set_motor_model(0, 0, 0, 0)

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)

PWM.close()

print("\n📊 INTERPRET RESULTS:")
print("-"*40)
print("✅ If wheels spin: Motors and wiring are good")
print("   → Issue is POWER (batteries) or TRACTION (surface)")
print("")
print("❌ If wheels don't spin: Check:")
print("   1. Battery voltage (measure with multimeter)")
print("   2. Motor driver board (LED should be on)")
print("   3. Wire connections (IN1,IN2,IN3,IN4)")
print("   4. Motor driver enable jumpers (ENA,ENB)")
print("")
print("🔋 Battery Requirements:")
print("   - Voltage: 7.4V - 12V")
print("   - Current: 15A+ continuous")
print("   - Recommended: 2x 18650 Li-ion (30Q, HG2, VTC6)")
print("="*70)
