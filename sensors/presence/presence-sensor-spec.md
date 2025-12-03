# 24G MmWave Radar Human Presence Sensor

## Smart Home Halacha Project - Hardware Documentation

---

## Overview

This document provides technical specifications and Zigbee2MQTT (Z2M) configuration details for the **Tuya ZG-204ZM** 24G MmWave Radar Human Presence Sensor, commonly available on AliExpress and similar platforms.

> **Note**: The product images shown are representative examples from AliExpress listings. Actual products may vary by seller.

---

## Product Images (AliExpress Samples)

*See attached screenshots showing typical AliExpress listings for this sensor type.*

**Key Features Advertised:**
- 24G Radar Presence Sensor
- PIR Infrared Detection
- Luminance Detection
- Temperature Detection
- Humidity Detection
- Works with Zigbee2MQTT

---

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| **Sensor Type A** | 24G Radar + PIR + Luminance + Temperature + Humidity |
| **Sensor Type B** | 24G Radar + PIR + Luminance |
| **Working Voltage** | DC 3V |
| **Power Adapter** | USB DC 5V |
| **Quiescent Current** | < 65uA |
| **Wireless Protocol** | Zigbee 3.0 (requires Zigbee gateway) |
| **App Support** | Smart Life / Tuya |
| **Illuminance Range** | 0-3500 Lux |
| **Battery Type** | 2x LR03 AAA (not included) |
| **Working Temperature** | -10C to 55C |
| **Working Humidity** | max 95% RH |

### Detection Capabilities

- **Static Detection (Radar)**: Maximum 3.5 meters, sensitivity adjustable
- **Motion Detection (PIR)**: Maximum 5 meters, fixed sensitivity
- **Light Value Updates**: Every 1 minute (on change)
- **Temperature/Humidity Updates**: Every 15 seconds (0.3C or 3% RH threshold)

### Important Operating Notes

1. Zigbee devices must be connected to a Zigbee gateway to function
2. After installation, align the sensing surface with the detection area
3. For frequent false negatives, set "Presence Keep Time" to 60+ seconds and sensitivity to 8x
4. Low-power device - settings update only when device uploads data or is triggered
5. When no presence detected, PIR activates first, then triggers mmWave radar for static detection

---

## Zigbee2MQTT Integration

### Device Identification

| Field | Value |
|-------|-------|
| **Zigbee Model** | ZG-204ZM |
| **Manufacturer** | HOBEIAN (PIR 24Ghz human presence sensor) |
| **Model** | ZG-204ZM (Tuya) |
| **MQTT Topic** | zigbee2mqtt/[device_name] |

### Exposed Parameters (Z2M Interface)

The following parameters are exposed via Zigbee2MQTT and can be adjusted:

#### Read-Only Values
- **Presence**: Boolean (true/false) - indicates if presence detected
- **Motion State**: Enum (none/small/large) - type of motion detected
- **Illuminance**: Integer (lux) - measured light level
- **Battery**: Percentage (%) - remaining battery
- **Link Quality**: Integer (lqi) - Zigbee signal strength

#### Configurable Parameters

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| **Fading Time** | 0-28800 | seconds | Presence keep time |
| **Static Detection Distance** | 0-6 | meters | Radar detection range |
| **Static Detection Sensitivity** | 0-10 | x | Radar sensitivity multiplier |
| **Indicator** | OFF/ON | - | LED indicator mode |
| **Motion Detection Mode** | only_pir / pir_and_radar / only_radar | - | Detection method selection |
| **Motion Detection Sensitivity** | 0-10 | x | PIR/motion sensitivity |

### Sample JSON State Payload

```json
{
  "battery": 100,
  "illuminance": 1528,
  "indicator": "OFF",
  "linkquality": 94,
  "motion_detection_mode": "only_pir",
  "motion_state": "small",
  "presence": true,
  "fading_time": null,
  "motion_detection_sensitivity": null,
  "static_detection_distance": null,
  "static_detection_sensitivity": null
}
```

---

## Potential Shabbat Solution: Sensitivity Threshold Workaround

> **Disclaimer**: This is a theoretical technical approach only. It has NOT been tested to confirm effectiveness, and no halachic determination has been made regarding whether this approach is permissible or advisable. Consult with a qualified posek before implementing any Shabbat automation strategy.

### The Concept

Since this sensor does not have a true "disable" option, one potential workaround is to set the detection thresholds to values that would effectively prevent any detection from occurring.

**Key Observation**: The Z2M interface allows toggling between PIR and radar modes, but does NOT provide an option to disable detection entirely.

### Proposed Settings (Pre-Shabbat)

| Parameter | Normal Value | Shabbat Value | Effect |
|-----------|-------------|---------------|--------|
| **Static Detection Distance** | 3-6 m | **0 m** | Radar won't detect at any distance |
| **Static Detection Sensitivity** | 5-8x | **0x** | Radar sensitivity at minimum |
| **Motion Detection Sensitivity** | 5-8x | **0x** | PIR sensitivity at minimum |

### Sample Home Assistant Automation

```yaml
# UNTESTED - Conceptual only
automation:
  - alias: "Presence Sensor - Pre-Shabbat Disable"
    trigger:
      - platform: state
        entity_id: binary_sensor.shabbat
        to: 'on'
    action:
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_presence/set"
          payload: >-
            {
              "static_detection_distance": 0,
              "static_detection_sensitivity": 0,
              "motion_detection_sensitivity": 0
            }

  - alias: "Presence Sensor - Post-Shabbat Enable"
    trigger:
      - platform: state
        entity_id: binary_sensor.shabbat
        to: 'off'
    action:
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_presence/set"
          payload: >-
            {
              "static_detection_distance": 4,
              "static_detection_sensitivity": 6,
              "motion_detection_sensitivity": 6
            }
```

### Critical Unknowns

#### Technical Questions (Require Testing)
1. Does sensitivity=0 actually prevent detection?
2. Does distance=0 work as expected?
3. What about the PIR sensor at minimum sensitivity?
4. Do settings persist across power cycles?
5. Is there latency in applying settings?

#### Halachic Questions (Require Rabbinic Consultation)
1. Is "effectively disabled" sufficient?
2. What if the settings don't fully prevent detection?
3. Is pre-Shabbat automation problematic?
4. Grama considerations if sensor is "armed" at 0 sensitivity

### Alternative Approaches

1. **Physical switch**: Install on USB power supply for manual disconnect
2. **Removable batteries**: Remove before Shabbat (impractical for multiple sensors)
3. **Disable automations only**: If sensor state changes without actions are permissible

---

## Z2M Screenshots Reference

The following screenshots from Zigbee2MQTT demonstrate the actual interface and available settings for this sensor:

1. **About Tab**: Device identification, model info, MQTT topic
2. **Exposes Tab**: All readable values and configurable parameters
3. **Settings Tab**: Device-level settings (debounce, disable, etc.)
4. **State Tab**: Raw JSON payload from device

---

*This document is part of the Smart Home Halacha project exploring the intersection of home automation and Jewish law.*

*Generated: December 2024*
