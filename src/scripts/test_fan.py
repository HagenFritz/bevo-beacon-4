#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import argparse

class FanCycleTester:
    def __init__(self, gpio_pin=18, frequency=500):
        """Initialize fan controller"""
        self.gpio_pin = gpio_pin
        self.frequency = frequency
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpio_pin, self.frequency)
        self.pwm.start(0)
        
        print(f"Fan controller initialized at {self.frequency}Hz on GPIO{self.gpio_pin}")
    
    def set_speed_immediate(self, speed):
        """Set fan speed immediately without ramping"""
        self.pwm.ChangeDutyCycle(speed)
        print(f"Fan speed: {speed}%")
    
    def startup_cycle(self):
        """Execute startup cycle: Off → 100% → 10%"""
        print("\n=== Startup Cycle ===")
        
        # Off
        print("Fan OFF")
        self.set_speed_immediate(0)
        time.sleep(5)
        
        # Power to 100%
        print("Fan 100% (startup)")
        self.set_speed_immediate(100)
        time.sleep(5)
    
    def speed_sweep(self, start_speed=10, end_speed=90, step=10):
        """Test speeds from start to end in steps"""
        print(f"\n=== Speed Sweep: {start_speed}% to {end_speed}% ===")
        
        speeds = list(range(start_speed, end_speed + 1, step))
        
        for speed in speeds:
            print(f"Testing {speed}%")
            self.startup_cycle()
            self.set_speed_immediate(speed)
            time.sleep(5)

def main():
    """Main function with command line argument parsing"""
    
    parser = argparse.ArgumentParser(description="BEVO Beacon V4 Fan Cycle Tester")
    parser.add_argument("--hz", type=int, default=500, 
                       help="PWM frequency in Hz (default: 500)")
    parser.add_argument("--gpio", type=int, default=18,
                       help="GPIO pin number (default: 18)")
    
    args = parser.parse_args()
    
    print(f"BEVO Beacon V4 Fan Controller")
    print(f"PWM Frequency: {args.hz}Hz")
    print(f"GPIO Pin: {args.gpio}")
    print("=" * 40)
    
    fan_controller = FanCycleTester(gpio_pin=args.gpio, frequency=args.hz)
    
    fan_controller.speed_sweep()

if __name__ == "__main__":
    main()