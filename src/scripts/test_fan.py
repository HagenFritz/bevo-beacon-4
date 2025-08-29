#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

def test_frequency_range():
    """Test different PWM frequencies to find optimal fan control range"""
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    
    # Test frequencies (Hz)
    frequencies = [100, 200, 300, 500, 750, 1000, 1500, 2000, 5000, 10000, 25000]
    
    results = {}
    
    print("PWM Frequency Optimization Test")
    print("===============================")
    print("For each frequency, we'll test minimum working duty cycle")
    print()
    
    for freq in frequencies:
        print(f"\n--- Testing {freq}Hz ---")
        
        fan_pwm = GPIO.PWM(18, freq)
        fan_pwm.start(0)
        
        # Test duty cycles from low to high
        min_working_duty = None
        
        for duty in range(5, 101, 5):
            fan_pwm.ChangeDutyCycle(duty)
            time.sleep(2)  # Let fan stabilize
            
            response = input(f"  {duty}% duty @ {freq}Hz - Is fan spinning reliably? (y/n/q to quit): ")
            
            if response.lower() == 'q':
                fan_pwm.stop()
                return results
            elif response.lower() == 'y' and min_working_duty is None:
                min_working_duty = duty
                print(f"  ✅ Minimum working duty cycle: {duty}%")
                break
        
        fan_pwm.stop()
        
        if min_working_duty:
            control_range = 100 - min_working_duty
            results[freq] = {
                'min_duty': min_working_duty,
                'control_range': control_range,
                'usable_range': f"{min_working_duty}%-100%"
            }
            print(f"  Control range: {control_range}% ({min_working_duty}%-100%)")
        else:
            results[freq] = {
                'min_duty': None,
                'control_range': 0,
                'usable_range': "None - fan didn't start"
            }
            print("  ❌ Fan didn't start at any duty cycle")
    
    return results

def analyze_results(results):
    """Analyze test results and recommend optimal frequency"""
    
    print("\n" + "="*50)
    print("FREQUENCY OPTIMIZATION RESULTS")
    print("="*50)
    
    # Print results table
    print(f"{'Frequency (Hz)':<12} {'Min Duty %':<10} {'Control Range':<14} {'Usable Range'}")
    print("-" * 60)
    
    best_freq = None
    best_range = 0
    
    for freq, data in results.items():
        min_duty = data['min_duty'] if data['min_duty'] else "N/A"
        control_range = data['control_range']
        usable_range = data['usable_range']
        
        print(f"{freq:<12} {str(min_duty):<10} {control_range}%{'':<10} {usable_range}")
        
        # Track best performance
        if control_range > best_range:
            best_range = control_range
            best_freq = freq
    
    print("\n" + "="*50)
    if best_freq:
        print(f"🎯 OPTIMAL FREQUENCY: {best_freq}Hz")
        print(f"   Best control range: {best_range}%")
        print(f"   Usable range: {results[best_freq]['usable_range']}")
        
        print(f"\n📝 RECOMMENDATION FOR BEVO BEACON:")
        print(f"   Use {best_freq}Hz PWM frequency")
        print(f"   Operating range: {results[best_freq]['min_duty']}%-100%")
        print(f"   This gives you {best_range}% of control authority")
        
        # Practical implications for air quality monitoring
        min_duty = results[best_freq]['min_duty']
        print(f"\n🌬️  AIRFLOW IMPLICATIONS:")
        print(f"   Low flow rate: {min_duty}% PWM (~{min_duty * 0.01:.1f} CFM)")
        print(f"   High flow rate: 100% PWM (~1.0 CFM)")
        print(f"   Variable range suitable for different measurement modes")
        
    else:
        print("❌ No frequencies provided adequate control")
        print("Consider different fan model or circuit modifications")

def quick_test_specific_frequency(frequency):
    """Quick test of a specific frequency"""
    print(f"\n=== Quick Test: {frequency}Hz ===")
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    fan_pwm = GPIO.PWM(18, frequency)
    
    try:
        fan_pwm.start(0)
        
        test_duties = [25, 35, 45, 55, 65, 75, 85, 95]
        
        for duty in test_duties:
            fan_pwm.ChangeDutyCycle(duty)
            print(f"Testing {duty}%...")
            time.sleep(2)
            
            # Auto-advance version - just observe
            
        print("Test complete - did you see smooth speed control?")
        
    finally:
        fan_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Full frequency optimization (thorough)")
    print("2. Quick test of 500Hz (since it worked)")
    print("3. Test custom frequency")
    
    choice = input("\nEnter choice (1/2/3): ")
    
    if choice == "1":
        results = test_frequency_range()
        if results:
            analyze_results(results)
    elif choice == "2":
        quick_test_specific_frequency(500)
    elif choice == "3":
        freq = int(input("Enter frequency to test (Hz): "))
        quick_test_specific_frequency(freq)
    else:
        print("Invalid choice")
    
    GPIO.cleanup()