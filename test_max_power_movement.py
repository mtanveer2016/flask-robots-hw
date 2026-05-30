from motor import Ordinary_Car
import time

print("="*60)
print("MAX POWER TEST - Robot on GROUND")
print("="*60)

PWM = Ordinary_Car()

# Try to increase PWM duty cycle if your library supports it
try:
    PWM.pwm.set_dutycycle(100)
    print("✅ Set PWM to 100%")
except:
    print("⚠️ Could not set PWM, using default")

input("\nPress ENTER for MAX POWER FORWARD (3 seconds)...")
print("🔴 MAX FORWARD - Robot should move!")
PWM.set_motor_model(1, 0, 1, 0)
time.sleep(3)
PWM.set_motor_model(0, 0, 0, 0)
print("⚫ STOP")

print("\n" + "="*60)
print("If robot moved: Power was the issue")
print("If robot didn't move: Check mechanical/battery")
print("="*60)
