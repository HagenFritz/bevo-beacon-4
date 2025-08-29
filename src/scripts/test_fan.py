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
        
        # Drop to 10%
        print("Fan 10% (drop from startup)")
        self.set_speed_immediate(10)
        time.sleep(5)
    
    def speed_sweep(self, start_speed=10, end_speed=90, step=10):
        """Test speeds from start to end in steps"""
        print(f"\n=== Speed Sweep: {start_speed}% to {end_speed}% ===")
        
        speeds = list(range(start_speed, end_speed + 1, step))
        
        for speed in speeds:
            print(f"Testing {speed}%")
            self.set_speed_immediate(speed)
            time.sleep(5)
    
    def full_test_cycle(self):
        """Execute complete test: startup cycle + speed sweep"""
        try:
            # Startup cycle first
            self.startup_cycle()
            
            # Continue with speed sweep from 10% to 90%
            self.speed_sweep(start_speed=10, end_speed=90, step=10)
            
            # Final shutdown
            print("\n=== Shutdown ===")
            print("Fan OFF")
            self.set_speed_immediate(0)
            time.sleep(2)
            
            print("✅ Test cycle complete")
            
        except KeyboardInterrupt:
            print("\nTest interrupted by user")
        
        finally:
            self.cleanup()
    
    def interactive_mode(self):
        """Interactive speed control"""
        print(f"\nInteractive Mode (PWM @ {self.frequency}Hz)")
        print("Commands:")
        print("  0-100: Set speed percentage")
        print("  'startup': Run startup cycle")
        print("  'sweep': Run 10-90% sweep")
        print("  'q': Quit")
        
        try:
            while True:
                user_input = input("\nCommand: ").strip().lower()
                
                if user_input == 'q':
                    break
                elif user_input == 'startup':
                    self.startup_cycle()
                elif user_input == 'sweep':
                    self.speed_sweep()
                elif user_input.isdigit():
                    speed = int(user_input)
                    if 0 <= speed <= 100:
                        if speed > 0 and not self.is_running:
                            print("Fan not running - executing startup sequence first")
                            self.startup_cycle()
                            if speed != 10:  # If target isn't 10%, set it after startup
                                time.sleep(1)
                                self.set_speed_immediate(speed)
                        else:
                            self.set_speed_immediate(speed)
                            if speed == 0:
                                self.is_running = False
                    else:
                        print("Speed must be 0-100")
                else:
                    print("Invalid command")
        
        except KeyboardInterrupt:
            print("\nExiting interactive mode")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean shutdown"""
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete")

def main():
    """Main function with command line argument parsing"""
    
    parser = argparse.ArgumentParser(description="BEVO Beacon V4 Fan Cycle Tester")
    parser.add_argument("--hz", type=int, default=500, 
                       help="PWM frequency in Hz (default: 500)")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("--gpio", type=int, default=18,
                       help="GPIO pin number (default: 18)")
    
    args = parser.parse_args()
    
    print(f"BEVO Beacon V4 Fan Controller")
    print(f"PWM Frequency: {args.hz}Hz")
    print(f"GPIO Pin: {args.gpio}")
    print("=" * 40)
    
    fan_controller = FanCycleTester(gpio_pin=args.gpio, frequency=args.hz)
    
    if args.interactive:
        fan_controller.interactive_mode()
    else:
        fan_controller.full_test_cycle()

if __name__ == "__main__":
    main()