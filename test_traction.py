from motor import Ordinary_Car
import time

PWM = Ordinary_Car()

print("="*60)
print("TRACTION TEST")
print("="*60)
print("\nThis test compares motor performance on/off ground")
print("\nSTEP 1: LIFT robot so wheels are in the air")
input("Press ENTER when robot is LIFTED...")

print("\nTesting FORWARD (wheels in air)...")
PWM.set_motor_model(1, 0, 1, 0)
time.sleep(2)
PWM.set_motor_model(0, 0, 0, 0)
print("  ✓ Forward test complete")

print("\nSTEP 2: Place robot on GROUND")
input("Press ENTER when robot is on GROUND...")

print("\nTesting FORWARD (on ground)...")
PWM.set_motor_model(1, 0, 1, 0)
time.sleep(2)
PWM.set_motor_model(0, 0, 0, 0)

PWM.close()

print("\n" + "="*60)
print("RESULTS:")
print("- If wheels spin in air but NOT on ground:")
print("  → POWER ISSUE - batteries can't provide enough current")
print("  → Solution: Use high-drain 18650 batteries")
print("- If wheels DON'T spin in air:")
print("  → WIRING ISSUE - check connections")
print("="*60)
