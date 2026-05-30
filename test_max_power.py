from motor import Ordinary_Car
import time

PWM = Ordinary_Car()

print("="*60)
print("MAX POWER MOTOR TEST")
print("="*60)

# For Freenove motors, full speed is set by the motor model
# The PWM duty cycle is handled internally by the library

print("\n1. Testing FORWARD at maximum speed...")
PWM.set_motor_model(1, 0, 1, 0)  # Full forward
print("   Motors should spin FORWARD at max speed")
time.sleep(3)

print("\n2. Testing BACKWARD at maximum speed...")
PWM.set_motor_model(0, 1, 0, 1)  # Full backward
print("   Motors should spin BACKWARD at max speed")
time.sleep(3)

print("\n3. Testing LEFT turn...")
PWM.set_motor_model(0, 1, 1, 0)  # Left turn
print("   Robot should turn LEFT")
time.sleep(2)

print("\n4. Testing RIGHT turn...")
PWM.set_motor_model(1, 0, 0, 1)  # Right turn
print("   Robot should turn RIGHT")
time.sleep(2)

print("\n5. STOPPING motors...")
PWM.set_motor_model(0, 0, 0, 0)
print("   Motors stopped")

PWM.close()

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nIf wheels didn't spin:")
print("  1. Lift robot off ground and test again")
print("  2. Check battery voltage (needs 7.4V+)")
print("  3. Check motor wire connections")
print("="*60)
