#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

def setup_fan():
    """Initialize GPIO and PWM for fan control"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    fan_pwm = GPIO.PWM(18, 1000)  # 1000Hz frequency
    return fan_pwm

def test_basic_on_off(fan_pwm):
    """Simple on/off test"""
    print("\n=== Basic On/Off Test ===")
    
    print("Fan OFF...")
    fan_pwm.start(0)
    time.sleep(3)
    
    print("Fan ON at 50%...")
    fan_pwm.ChangeDutyCycle(50)
    time.sleep(3)
    
    print("Fan OFF...")
    fan_pwm.ChangeDutyCycle(0)
    time.sleep(2)

def test_speed_ramp(fan_pwm):
    """Test gradual speed increase"""
    print("\n=== Speed Ramp Test ===")
    
    fan_pwm.start(0)
    
    # Slow ramp up
    for duty in range(10, 101, 10):
        fan_pwm.ChangeDutyCycle(duty)
        print(f"Fan speed: {duty}%")
        time.sleep(2)
    
    # Ramp down
    for duty in range(100, 9, -10):
        fan_pwm.ChangeDutyCycle(duty)
        print(f"Fan speed: {duty}%")
        time.sleep(1)
    
    fan_pwm.ChangeDutyCycle(0)
    print("Fan stopped")

def test_specific_speeds(fan_pwm):
    """Test specific operating points"""
    print("\n=== Specific Speed Test ===")
    
    speeds = [15, 25, 50, 75, 100]
    
    for speed in speeds:
        fan_pwm.ChangeDutyCycle(speed)
        print(f"Testing {speed}% speed for 5 seconds...")
        time.sleep(5)
    
    fan_pwm.ChangeDutyCycle(0)

def main():
    """Run all tests"""
    print("BEVO Beacon V4 Fan Controller Test")
    print("==================================")
    
    fan_pwm = setup_fan()
    
    try:
        # Run test sequence
        test_basic_on_off(fan_pwm)
        
        input("\nPress Enter to continue to speed ramp test...")
        test_speed_ramp(fan_pwm)
        
        input("\nPress Enter to test specific operating speeds...")
        test_specific_speeds(fan_pwm)
        
        print("\n✅ All tests complete!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    
    finally:
        fan_pwm.stop()
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()