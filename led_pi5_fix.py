# -*-coding: utf-8 -*-
import time
from parameter import ParameterManager
from rpi_ledpixel import Freenove_RPI_WS281X
from spi_ledpixel import Freenove_SPI_LedPixel

class Led:
    def __init__(self):
        """Initialize the Led class for Pi 5 compatibility."""
        self.param = ParameterManager()
        self.connect_version = self.param.get_connect_version()
        self.pi_version = self.param.get_raspberry_pi_version()
        
        print(f"   Connect Version: {self.connect_version}")
        print(f"   Pi Version: {self.pi_version}")

        # FORCE LED to work on Pi 5
        if self.pi_version == 2:
            print("   ⚠️  Pi 5 detected - forcing LED compatibility")
            try:
                self.strip = Freenove_SPI_LedPixel(8, 255, 'GRB')
                self.is_support_led_function = True
                print("   ✅ LED initialized with SPI mode")
            except Exception as e:
                print(f"   ❌ SPI mode failed: {e}")
                self.is_support_led_function = False
        elif self.connect_version == 1 and self.pi_version == 1:
            self.strip = Freenove_RPI_WS281X(8, 255, 'RGB')
            self.is_support_led_function = True
        elif self.connect_version == 2 and (self.pi_version == 1 or self.pi_version == 2):
            self.strip = Freenove_SPI_LedPixel(8, 255, 'GRB')
            self.is_support_led_function = True
        else:
            print(f"   ❌ Unsupported combination")
            self.is_support_led_function = False
                    
        self.start = time.time()
        self.next = 0
        self.color_wheel_value = 100
        self.color_chase_rainbow_index = 0
        self.color_wipe_index = 0
        self.rainbowbreathing_brightness = 0

    def colorBlink(self, state=1, wait_ms=300):
        if not self.is_support_led_function:
            return
        if state == 1:
            color = [[255,0,0],[0,0,0],[0,255,0],[0,0,0],[0,0,255],[0,0,0]]
            self.next = time.time()
            if (self.next - self.start) > wait_ms / 1000.0:
                self.start = self.next
                for i in range(self.strip.get_led_count()):
                    self.strip.set_led_rgb_data(i, color[self.color_wipe_index%4])
                    self.strip.show()
                self.color_wipe_index += 1
        else:
            self.strip.set_all_led_color(0, 0, 0)
            self.strip.show()

    def wheel(self, pos):
        if not self.is_support_led_function:
            return (0,0,0)
        if pos < 0 or pos > 255:
            return (0,0,0)
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)
        
    def rainbowbreathing(self, wait_ms=10):
        if not self.is_support_led_function:
            return
        self.next = time.time()
        if (self.next - self.start) > wait_ms / 1000.0:
            self.start = self.next
            color1 = self.wheel(self.color_wheel_value % 255)
            if (self.rainbowbreathing_brightness % 200) > 100:
                brightness = 200 - self.rainbowbreathing_brightness
            else:
                brightness = self.rainbowbreathing_brightness
            color2 = [int(color1[0] * brightness / 100), int(color1[1] * brightness / 100), int(color1[2] * brightness / 100)]
            for i in range(self.strip.get_led_count()):
                self.strip.set_led_rgb_data(i, color2)
            self.strip.show()
            self.rainbowbreathing_brightness += 1  
            if self.rainbowbreathing_brightness >= 200:
                self.rainbowbreathing_brightness = 0
                self.color_wheel_value += 32
                if self.color_wheel_value >= 256:
                    self.color_wheel_value = 0

    def rainbowCycle(self, wait_ms=20):
        if not self.is_support_led_function:
            return
        self.next = time.time()
        if (self.next - self.start > wait_ms / 1000.0):
            self.start = self.next
            for i in range(self.strip.get_led_count()):
                self.strip.set_led_rgb_data(i, self.wheel((int(i * 256 / self.strip.get_led_count()) + self.color_wheel_value) & 255))
            self.strip.show()
            self.color_wheel_value += 1
            if self.color_wheel_value >= 256:
                self.color_wheel_value = 0

    def following(self, wait_ms=50):
        if not self.is_support_led_function:
            return
        self.next = time.time()
        if (self.next - self.start > wait_ms / 1000.0):
            self.start = self.next
            for i in range(self.strip.get_led_count()):
                self.strip.set_led_rgb_data(i, [0, 0, 0])
            self.strip.set_led_rgb_data(self.color_chase_rainbow_index, self.wheel(self.color_wheel_value & 255))
            self.strip.show()
            self.color_chase_rainbow_index += 1
            if self.color_chase_rainbow_index >= self.strip.get_led_count():
                self.color_chase_rainbow_index = 0
            self.color_wheel_value += 5
            if self.color_wheel_value >= 256:
                self.color_wheel_value = 0
               
    def ledIndex(self, index, R, G, B):
        if not self.is_support_led_function:
            print("  ⚠️ LED not supported")
            return
        color = (R, G, B)
        for i in range(8):
            if index & 0x01 == 1:
                self.strip.set_led_rgb_data(i, color)
                self.strip.show()
            index = index >> 1

if __name__ == '__main__':
    print('Testing LED on Pi 5...')
    led = Led()       
    try:
        for i in range(2):
            led.ledIndex(0xFF, 255, 0, 0)
            time.sleep(0.5)
            led.ledIndex(0xFF, 0, 255, 0)
            time.sleep(0.5)
            led.ledIndex(0xFF, 0, 0, 255)
            time.sleep(0.5)
        led.ledIndex(0xFF, 0, 0, 0)
        print("LED test complete!")
    except KeyboardInterrupt:
        led.ledIndex(0xFF, 0, 0, 0)
