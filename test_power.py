from motor import Ordinary_Car
import time

print("="*60)
print("MOTOR POWER TEST")
print("="*60)

PWM = Ordinary_Car()

print("\n1. Testing FORWARD at MAX power...")
PWM.set_motor_model(1, 0, 1, 0)
time.sleep(3)
print("   ✓ Forward test complete")

print("\n2. Testing BACKWARD at MAX power...")
PWM.set_motor_model(0, 1, 0, 1)
time.sleep(3)
print("   ✓ Backward test complete")

print("\n3. Testing LEFT turn...")
PWM.set_motor_model(0, 1, 1, 0)
time.sleep(2)
print("   ✓ Left turn test complete")

print("\n4. Testing RIGHT turn...")
PWM.set_motor_model(1, 0, 0, 1)
time.sleep(2)
print("   ✓ Right turn test complete")

print("\n5. Stopping motors...")
PWM.set_motor_model(0, 0, 0, 0)
print("   ✓ Stopped")

PWM.close()
print("\n" + "="*60)
print("If wheels didn't move, check:")
print("   - Battery voltage (should be 7.4V-12V)")
print("   - Battery connections")
print("   - Motor driver power LED")
print("="*60)
