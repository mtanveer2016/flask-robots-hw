#!/usr/bin/env python3
import lgpio
import time
import RPi.GPIO as GPIO

print("="*70)
print("COMPLETE HARDWARE DIAGNOSTIC")
print("="*70)

# ============================================
# Check 1: LED/Buzzer (already working)
# ============================================
print("\n1. ✓ Buzzer/LED works (you heard the beep)")

# ============================================
# Check 2: GPIO pin test with multimeter instructions
# ============================================
print("\n2. GPIO SIGNAL TEST (Use a multimeter or LED+resistor)")
print("   " + "-"*50)
print("   Measure voltage between each GPIO pin and GND:")
print("")
print("   When you press ENTER, each pin will go HIGH (3.3V)")
print("   If you see 3.3V on your meter, the Pi is working.")
print("")

input("   Press ENTER to test GPIO 13...")
handle = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(handle, 13)
lgpio.gpio_write(handle, 13, 1)
print("   >>> GPIO 13 = HIGH (3.3V) - Measure now!")
time.sleep(3)
lgpio.gpio_write(handle, 13, 0)
print("   >>> GPIO 13 = LOW (0V)")

input("\n   Press ENTER to test GPIO 21...")
lgpio.gpio_claim_output(handle, 21)
lgpio.gpio_write(handle, 21, 1)
print("   >>> GPIO 21 = HIGH (3.3V) - Measure now!")
time.sleep(3)
lgpio.gpio_write(handle, 21, 0)
print("   >>> GPIO 21 = LOW (0V)")

input("\n   Press ENTER to test GPIO 17...")
lgpio.gpio_claim_output(handle, 17)
lgpio.gpio_write(handle, 17, 1)
print("   >>> GPIO 17 = HIGH (3.3V) - Measure now!")
time.sleep(3)
lgpio.gpio_write(handle, 17, 0)
print("   >>> GPIO 17 = LOW (0V)")

input("\n   Press ENTER to test GPIO 27...")
lgpio.gpio_claim_output(handle, 27)
lgpio.gpio_write(handle, 27, 1)
print("   >>> GPIO 27 = HIGH (3.3V) - Measure now!")
time.sleep(3)
lgpio.gpio_write(handle, 27, 0)
print("   >>> GPIO 27 = LOW (0V)")

lgpio.gpiochip_close(handle)

# ============================================
# Check 3: Motor driver power
# ============================================
print("\n3. MOTOR DRIVER POWER CHECK")
print("   " + "-"*50)
print("   Answer these questions:")
print("   □ Is the motor driver power LED ON?")
print("   □ Is the battery connected to motor driver VCC?")
print("   □ Is the battery voltage between 7.4V and 12V?")
print("   □ Is the battery ground connected to motor driver GND?")
print("   □ Is the battery ground also connected to Pi GND?")
print("   □ Are the ENA and ENB jumpers installed?")

# ============================================
# Check 4: Motor test with direct battery
# ============================================
print("\n4. DIRECT MOTOR TEST")
print("   " + "-"*50)
print("   To test if motors work:")
print("   1. Disconnect motor from driver")
print("   2. Connect motor wires directly to battery (briefly!)")
print("   3. Motor should spin strongly")
print("")
print("   If motor spins → Driver or wiring issue")
print("   If motor doesn't spin → Motor is dead")

# ============================================
# Check 5: Motor driver output test
# ============================================
print("\n5. MOTOR DRIVER OUTPUT TEST")
print("   " + "-"*50)
print("   With robot LIFTED off ground:")
print("   1. Run this script's motor test")
print("   2. Measure voltage at motor driver output terminals")
print("   3. Should read battery voltage when active")
print("   4. If 0V → Driver not enabled or dead")

print("\n" + "="*70)
print("MOST COMMON ISSUES (Based on 'beep but no movement')")
print("="*70)
print("""
┌─────────────────────────────────────────────────────────────┐
│  ISSUE                    │  SOLUTION                       │
├───────────────────────────┼─────────────────────────────────┤
│  No power to motor driver │ Connect battery to driver VCC   │
│  Driver enable jumpers    │ Install ENA and ENB jumpers     │
│  No common ground         │ Connect battery GND to Pi GND   │
│  Low battery voltage      │ Use 7.4V-12V (2x18650)          │
│  Wrong wiring             │ Check IN1→13, IN2→21, etc.      │
│  Dead motor driver        │ Replace L298N/L293D board       │
│  Motor wires disconnected │ Check connections at motors     │
└─────────────────────────────────────────────────────────────┘
""")
