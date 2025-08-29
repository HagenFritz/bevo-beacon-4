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

## Step 7: GPIO Testing and Code Repository Setup

### Clone the BEVO Beacon V4 Repository

```bash
cd ~
git clone https://github.com/HagenFritz/bevo-beacon-4.git
cd bevo-beacon-4/src

# Activate virtual environment if not already active
python3 -m venv .venv
source .venv/bin/activate

# Install any additional dependencies
pip install -r requirements.txt  # if requirements file exists
```

### Breadboard LED Test Circuit

#### Components Required
- 1 LED (any color)
- 1x 1K ohm resistor (use this instead of 10K for visible brightness)
- 2 jumper wires (male-to-male)
- Breadboard

#### Circuit Wiring
```
Raspberry Pi GPIO 18 ──[1K resistor]──[LED+]──[LED-]── Raspberry Pi GND
```

**Physical Pin Connections:**
- **GPIO 18** (physical pin 12) → 1K resistor → LED long leg (positive/anode)
- **LED short leg** (negative/cathode) → **Ground** (physical pin 6)

#### Breadboard Layout
1. Insert LED into breadboard with legs in separate rows
2. Connect 1K resistor from LED positive leg to a nearby breadboard row
3. Connect jumper wire from GPIO 18 (pin 12) to the resistor row
4. Connect jumper wire from LED negative leg to Pi Ground (pin 6)

```
    Pi Header                 Breadboard
┌─────────────────┐         ┌────────────────┐
│  1●  ●2         │         │ [1K-R]──[LED+] │
│  3●  ●4         │         │         │      │
│  5●  ●6  GND────┼─────────┼─────────┘      │
│  7●  ●8         │         │  [LED-]────────│
│  9●  ●10        │         └────────────────┘
│ 11●  ●12 GPIO18─┼─────────────[to resistor]
│ 13●  ●14        │
└─────────────────┘
```

### Run GPIO Test Code

```bash
# Run the GPIO test script (replace with actual filename)
python3 src/scripts/test_gpio.py
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
