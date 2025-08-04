# BEVO Beacon V4 Project Overview

## Project Purpose

The BEVO Beacon V4 is an enhanced open-source indoor air quality monitoring system designed to address critical limitations of the original BEVO Beacon. This project builds upon graduate research work previously published in Building and Environment journal, incorporating lessons learned and modern improvements to create a more accurate, reliable, and comprehensive indoor air quality monitor.

### Original BEVO Beacon Background
The original Building EnVironment and Occupancy (BEVO) Beacon was an open-source indoor air quality monitoring system that measured up to 24 parameters at one-minute resolution. While successful, it had several limitations including sensor calibration challenges, thermal management issues, and limited pollutant coverage.

## Overall Goals

### Primary Objectives
1. **Improved Sensor Accuracy**: Address calibration issues from V1, particularly poor PM2.5 correlation (r=-0.13-0.91) and variable CO₂ performance (r=0.62-0.99)
2. **Enhanced Thermal Management**: Solve overheating problems that affected temperature/humidity sensor readings in the original design
3. **Controlled Airflow Design**: Implement systematic air sampling to improve sensor exposure and measurement accuracy
4. **Comprehensive Pollutant Detection**: Expand beyond basic parameters to include health-critical indoor pollutants
5. **Professional Reliability**: Create a research-grade instrument suitable for long-term deployment and scientific studies

### Design Philosophy
- **Open Source**: All hardware designs, software, and documentation will be publicly available
- **Research Grade**: Accuracy and reliability suitable for scientific research applications
- **Cost Effective**: Total system cost under $400 per unit
- **DIY Friendly**: Buildable by researchers and makers with standard tools
- **Modular Design**: Easy to modify, repair, and upgrade individual components

## Pollutants Being Measured

### Core Indoor Air Quality Parameters

#### 1. Carbon Dioxide (CO₂)
- **Sensor**: SenseAir S8 LP
- **Range**: 400-2000 ppm
- **Purpose**: Ventilation adequacy indicator, cognitive performance impact assessment
- **Health Relevance**: High CO₂ levels (>1000 ppm) associated with drowsiness, poor concentration, and inadequate ventilation

#### 2. Particulate Matter (PM2.5)
- **Sensor**: Honeywell HPMA115S0-XXX
- **Range**: 0-1000 μg/m³ 
- **Purpose**: Detection of fine airborne particles from outdoor pollution, cooking, combustion
- **Health Relevance**: PM2.5 linked to cardiovascular disease, respiratory illness, premature mortality

#### 3. Formaldehyde (HCHO)
- **Sensor**: Sensirion SFA30-D-T
- **Range**: 0-1000 ppb
- **Purpose**: Detection of off-gassing from furniture, building materials, adhesives
- **Health Relevance**: Known human carcinogen, common long-term indoor pollutant from wood products and furnishings

#### 4. Total Volatile Organic Compounds (TVOC)
- **Sensor**: Sensirion SGP41 (via SEK-SVM41 evaluation kit)
- **Range**: VOC Index 0-500
- **Purpose**: General indicator of chemical pollution from cleaning products, paints, materials
- **Health Relevance**: Various health impacts depending on specific compounds, general air quality indicator

#### 5. Nitrogen Oxides (NOx)
- **Sensor**: Sensirion SGP41 (via SEK-SVM41 evaluation kit)  
- **Range**: NOx Index 0-500
- **Purpose**: Detection of combustion byproducts, particularly from gas cooking appliances
- **Health Relevance**: Gas stove emissions can exceed 100 ppb, linked to childhood asthma and respiratory issues

#### 6. Temperature
- **Sensor**: Sensirion SHT41 (via Adafruit breakout)
- **Range**: -40°C to +125°C
- **Purpose**: Environmental monitoring, sensor compensation, comfort assessment
- **Application**: Thermal isolation validation, HVAC performance

#### 7. Relative Humidity  
- **Sensor**: Sensirion SHT41 (via Adafruit breakout)
- **Range**: 0-100% RH
- **Purpose**: Moisture monitoring, mold risk assessment, comfort evaluation
- **Application**: Building envelope performance, ventilation effectiveness

## System Architecture

### Computing Platform
- **Main Controller**: Raspberry Pi 4B (4GB RAM)
- **Storage**: 64GB MicroSD card
- **Power**: 5V 4A switching power supply
- **Connectivity**: Built-in WiFi for data transmission and remote monitoring

### Sensor Interface Strategy
- **5V Sensors**: SenseAir S8 (Modbus RTU communication)
- **3.3V Sensors**: All others (I2C and UART interfaces)
- **Level Shifting**: SparkFun bi-directional logic level converter for safe 5V↔3.3V communication
- **Power Distribution**: Single 5V supply with regulated distribution to all components

### Fan Control System
- **Fan**: Adafruit 3368 (5V, 30mm axial fan)
- **Speed Control**: Custom PWM controller circuit using 2N2222A transistor and 2N7002K MOSFET
- **Control Range**: 10-100% speed for precise airflow management
- **Purpose**: Controlled air sampling through sensor chamber

## Airflow Design Philosophy

### Core Principles
1. **Controlled Air Sampling**: Ensure all sensors receive representative air samples
2. **Sequential Exposure**: Air flows past sensors in series to prevent cross-contamination
3. **Measurable Flow Rate**: Known airflow velocity enables enhanced concentration calculations
4. **Fresh Air Supply**: Continuous air exchange prevents sensor saturation
5. **Thermal Isolation**: Separate airflow path keeps sensors at stable temperature

### Airflow Path Design
```
Intake (with filter) → Fan → Sensor Chamber → Exhaust
                              ↓
                    CO₂ → PM2.5 → HCHO → TVOC/NOx → T/RH
```

### Airflow Specifications
- **Target Flow Rate**: 0.5-1.0 CFM (controlled by PWM fan speed)
- **Air Path**: Sequential sensor exposure to prevent interference
- **Mixing**: Adequate residence time for sensor response without turbulence
- **Filtration**: Basic pre-filter to prevent dust accumulation on sensors

### Benefits of Controlled Airflow
- **Improved Response Time**: Active air delivery vs. passive diffusion
- **Better Sensor Accuracy**: Representative sampling vs. stagnant air pockets  
- **Thermal Stability**: Continuous airflow prevents heat buildup
- **Calibration Enhancement**: Flow rate data improves concentration calculations
- **Consistent Performance**: Reduced variability from air movement variations

## 3D Printed Housing Design

### Design Requirements
- **Material**: PETG filament for temperature resistance and chemical compatibility
- **Dual Chamber Architecture**: Separate electronics and sensor compartments
- **Thermal Isolation**: Physical barrier between heat-generating electronics and sensors
- **Accessibility**: Easy assembly/disassembly for maintenance and calibration
- **Mounting Options**: Tabletop deployment (wall mounting not required)

### Chamber Configuration
#### Electronics Chamber (Upper)
- Houses Raspberry Pi, power supply, interface electronics
- Heat dissipation design with ventilation
- Cable management and strain relief
- Status LED visibility

#### Sensor Chamber (Lower)  
- All sensors mounted in controlled airflow path
- Thermal isolation from electronics heat
- Easy sensor access for calibration
- Integrated airflow channels

### Airflow Integration
- **Intake Design**: Filtered air entry with fan mounting
- **Internal Ducting**: Channels directing air past each sensor sequentially  
- **Exhaust Ports**: Controlled air exit to maintain proper flow
- **Sensor Mounting**: Optimal positioning for air exposure without interference

### Manufacturing Considerations
- **Print-in-Place**: Minimize assembly complexity where possible
- **Threaded Inserts**: Brass heat-set inserts for robust mechanical connections
- **Gasket Compatibility**: Designed for TPU seals where airtight connections needed
- **Wire Management**: Integrated channels and strain relief

## Complete Bill of Materials

### Core Electronics
| Component | Manufacturer | Part Number | Quantity | Purpose |
|-----------|--------------|-------------|----------|---------|
| Raspberry Pi 4B | Raspberry Pi Foundation | SC0194(9) | 1 | Main controller |
| 5V Power Supply | Raspberry Pi Foundation | SC1412 | 1 | System power |
| MicroSD Card | SanDisk | 64GB Class 10 | 1 | Storage |
| Logic Level Shifter | SparkFun | BOB-12009 | 1 | 5V↔3.3V interface |

### Sensors
| Component | Manufacturer | Part Number | Quantity | Measures |
|-----------|--------------|-------------|----------|----------|
| CO₂ Sensor | SenseAir | S8 LP 004-0-0053 | 1 | Carbon dioxide |
| PM Sensor | Honeywell | HPMA115S0-XXX | 1 | Particulate matter |
| Formaldehyde Sensor | Sensirion | SFA30-D-T | 1 | HCHO |
| TVOC/NOx Sensor | Sensirion | SEK-SVM41 | 1 | VOCs, nitrogen oxides |
| Temp/Humidity Sensor | Adafruit | 5776 (SHT41) | 1 | Temperature, humidity |

### Airflow Management
| Component | Manufacturer | Part Number | Quantity | Purpose |
|-----------|--------------|-------------|----------|---------|
| Fan | Adafruit | 3368 | 2 | Controlled airflow |
| BJT Transistor | Central Semiconductor | 2N2222A PBFREE | 1 | PWM control |
| MOSFET | Diodes Inc | 2N7002K-7 | 1 | PWM switching |
| Resistors | Stackpole | CF14JT1K00, CF14JT10K0 | 10 each | PWM circuit |

### Interface Components
| Component | Manufacturer | Part Number | Quantity | Purpose |
|-----------|--------------|-------------|----------|---------|
| Terminal Blocks | Phoenix Contact | 1715022 | 8 | Sensor connections |
| Breadboard | Adafruit | 8808 | 1 | Prototyping |
| Wire & Connectors | Various | Mixed | 1 set | Interconnections |

### 3D Printing Materials
| Component | Type | Quantity | Purpose |
|-----------|------|----------|---------|
| PETG Filament | 3D Printing | ~200g | Main housing |
| TPU Filament | 3D Printing | ~50g | Gaskets, seals |
| Threaded Inserts | Brass M3x5mm | 20 | Mechanical fastening |
| Screws | M3 Socket Head | 30 | Assembly hardware |

## Success Metrics

### Performance Targets
- **CO₂ Accuracy**: ±30 ppm vs reference instruments
- **PM2.5 Correlation**: r > 0.9 with calibrated reference
- **Thermal Stability**: Sensor chamber within ±2°C of ambient
- **Operational Reliability**: >99% uptime over continuous deployment
- **Calibration Stability**: <5% drift over 6 months
- **Assembly Time**: <4 hours for experienced maker

### Applications
This project represents a significant advancement in open-source indoor air quality monitoring, combining research-grade accuracy with maker-friendly construction and comprehensive pollutant detection capabilities.

- Building performance assessment
- Indoor air quality research studies  
- HVAC system optimization
- Occupant health and productivity studies
- Environmental justice monitoring
- Building code and standard development
