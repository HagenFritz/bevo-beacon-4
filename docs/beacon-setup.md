# BEVO Beacon V4 - Raspberry Pi Setup Guide

## Hardware Requirements

### Essential Components
- Raspberry Pi 4B (4GB RAM recommended)
- 64GB MicroSD card (Class 10 or better)
- 5V 4A power supply
- USB keyboard
- MicroSD card reader/formatter

## Step 1: Flash Raspberry Pi OS

### Download and Install
1. Download **Raspberry Pi Imager** from https://www.raspberrypi.org/software/
2. Insert 64GB MicroSD card into your computer
3. Open Raspberry Pi Imager

### Configure the Image
1. Choose **"Raspberry Pi OS Lite (64-bit)"** (no desktop GUI)
2. Select your SD card
3. **Before writing**, click the gear icon (⚙️) for advanced options:
   - **Enable SSH** with password authentication
   - **Set username/password** (record these - you'll need them)
   - **Set locale settings** to your timezone
4. Write the image to SD card

### Initial Boot
1. Insert SD card into Pi 4B
2. Connect micro HDMI cable, keyboard, and power
3. Power on and wait for boot to complete

## Step 2: Network Configuration

### Modern Method (NetworkManager)
Modern Raspberry Pi OS uses NetworkManager instead of the old wpa_supplicant method.

#### Connect to WiFi
```bash
# Scan for available networks
sudo nmcli dev wifi rescan

# List visible networks
nmcli dev wifi list

# Connect to your network (replace with actual credentials)
sudo nmcli dev wifi connect "YourNetworkName" password "YourPassword"
```

#### Verify Connection
```bash
# Check connection status
iwconfig wlan0

# Get IP address
hostname -I

# Test internet connectivity
ping -c 3 google.com
```

## Step 3: System Updates and SSH Setup

### Update the System
```bash
sudo apt update && sudo apt upgrade -y
```

### Enable and Start SSH
```bash
# Install SSH server (if not already installed)
sudo apt install -y openssh-server

# Enable SSH service
sudo systemctl enable ssh
sudo systemctl start ssh

# Verify SSH is running
sudo systemctl status ssh
```

### Test SSH Connection
From your development computer:
```bash
# Use the username and IP from your Pi
ssh [username]@[pi_ip_address]

# Example:
ssh hfritz@172.20.10.11
```

## Step 4: Enable Hardware Interfaces

### Configure Hardware Interfaces
```bash
sudo raspi-config
```

Navigate to **3 Interface Options**:
- **I5 I2C** → Enable (required for most sensors)
- **I6 Serial Port** → Enable
  - "Login shell over serial?" → **No**
  - "Serial port hardware enabled?" → **Yes**

### Reboot to Apply Changes
```bash
sudo reboot
```

## Step 5: Install Development Environment

### Install System Packages
```bash
# Python development essentials
sudo apt install -y python3-pip python3-venv python3-dev

# Hardware interface tools
sudo apt install -y i2c-tools python3-smbus python3-rpi.gpio

# Serial communication tools
sudo apt install -y python3-serial minicom

# Development utilities
sudo apt install -y git vim nano tree htop

# Scientific computing packages
sudo apt install -y python3-numpy python3-scipy python3-matplotlib python3-pandas
```

## Step 6: Verify Hardware Interfaces

### Test I2C Interface
```bash
# Should show empty grid (no devices connected yet)
sudo i2cdetect -y 1
```

### Test GPIO Access
Create a simple GPIO test:
```bash
nano gpio_test.py
```

Add this code:
```python
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Simple blink test
for i in range(5):
    GPIO.output(18, True)
    time.sleep(0.5)
    GPIO.output(18, False)
    time.sleep(0.5)
    
GPIO.cleanup()
print("GPIO test completed successfully!")
```

Run the test:
```bash
python3 gpio_test.py
```

## Troubleshooting

### WiFi Connection Issues
- **Special characters**: Avoid WiFi names with apostrophes or complex symbols
- **Use nmcli**: Modern Pi OS requires NetworkManager commands, not wpa_supplicant.conf editing
- **Corporate networks**: May block SSH - use phone hotspot as alternative

### SSH Connection Issues
- **Connection refused**: SSH service not running - install and start openssh-server
- **Connection timeout**: Network firewall blocking SSH - try different network
- **Wrong credentials**: Verify username with `whoami` command on Pi

### Hardware Interface Issues
- **I2C not working**: Ensure enabled in raspi-config and reboot
- **Serial conflicts**: Make sure login shell over serial is disabled
- **Permission errors**: Add user to gpio group: `sudo usermod -a -G gpio $USER`

## Next Steps

With this foundation complete, you're ready to proceed with:

1. **PWM Fan Controller Circuit** assembly and testing
2. **Power System Validation** with all components
3. **Sensor Integration** starting with SHT41 (temperature/humidity)
4. **Software Development** for unified data collection

## Key Learnings

- **NetworkManager vs wpa_supplicant**: Modern Pi OS uses NetworkManager; ignore outdated wpa_supplicant tutorials
- **SSH on institutional networks**: Often blocked; phone hotspot provides reliable alternative
- **Micro vs Mini HDMI**: Pi 4B uses micro HDMI (smallest size), not mini HDMI
- **Pi OS Lite**: No GUI, all configuration via command line

## Estimated Setup Time
- Initial setup and flashing: 30 minutes
- Network configuration and troubleshooting: 15-45 minutes (depending on network complexity)
- Development environment installation: 20 minutes
- Total: 1-2 hours for complete foundation setup