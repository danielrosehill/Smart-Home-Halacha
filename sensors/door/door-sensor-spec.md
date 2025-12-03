# Door/Window Contact Sensor (Intrusion Sensor)

## Smart Home Halacha Project - Hardware Documentation

---

## Overview

This document provides technical specifications and Zigbee2MQTT (Z2M) configuration details for **Zigbee door/window contact sensors**, commonly used for intrusion detection in smart home setups. The examples shown include the popular **Aqara MCCGQ11LM** and similar **Tuya TS0203** models.

> **Note**: The product images shown are representative examples from AliExpress listings. Actual products may vary by seller.

---

## Product Images (AliExpress Samples)

*See attached screenshots showing typical AliExpress listings for door/window sensors.*

**Key Features Advertised:**
- Low-Profile Mini Design
- No Wiring Required
- Installation Free (No Screw Required)
- 2-Year Battery Life
- Works with Mi Home App
- Works with Apple HomeKit (Aqara models)
- 1 Year Warranty

---

## Technical Specifications

### Aqara MCCGQ11LM

| Parameter | Value |
|-----------|-------|
| **Model** | MCCGQ11LM |
| **Battery** | CR1632 (included) |
| **Wireless Protocol** | Zigbee |
| **Dimensions** | 41 x 22 x 11 mm (1.61 x 0.87 x 0.43 in.) |
| **Maximum Detection Distance** | 22 mm |
| **Operating Temperature** | -10C to +45C (14F to 113F) |
| **Operating Humidity** | 0-95% RH, non-condensing |
| **App Support** | Apple Home (iOS 10.3+), Aqara Home (Android 5.0+, iOS 10.3+), Mi Home |

### Tuya TS0203 (Alternative)

| Parameter | Value |
|-----------|-------|
| **Zigbee Model** | TS0203 |
| **Manufacturer** | _TZ3000_oxslv1c9 |
| **Type** | Door/window sensor |
| **Protocol** | Zigbee 3.0 |

---

## Operating Principle

Door/window contact sensors use a **magnetic reed switch** mechanism:

1. **Main Unit**: Contains the reed switch and Zigbee radio
2. **Magnet**: Small magnetic piece attached to the moving part (door/window)
3. **Detection**: When magnet is near (door closed), circuit is closed; when separated (door open), circuit opens
4. **Detection Distance**: Typically 15-22mm maximum gap for reliable detection

### Sensor States

| Physical State | Sensor Reading | Contact Value |
|----------------|----------------|---------------|
| Door/Window Closed | Magnet Near | `true` (Closed) |
| Door/Window Open | Magnet Far | `false` (Open) |

---

## Zigbee2MQTT Integration

### Device Identification (Tuya TS0203 Example)

| Field | Value |
|-------|-------|
| **Zigbee Model** | TS0203 |
| **Description** | Door/window sensor |
| **Manufacturer** | Tuya |
| **MQTT Topic** | zigbee2mqtt/[device_name] |
| **Support Status** | Supported: native |

### Exposed Parameters (Z2M Interface)

The door/window sensor exposes the following values:

| Parameter | Type | Description |
|-----------|------|-------------|
| **Contact** | Boolean | Indicates if contact is closed (true) or open (false) |
| **Battery** | Percentage | Remaining battery (may take up to 24 hours to report) |
| **Voltage** | Integer (mV) | Battery voltage in millivolts |
| **Tamper** | Boolean | Indicates if device has been tampered with |
| **Link Quality** | Integer (lqi) | Zigbee signal strength |
| **Battery Low** | Boolean | Low battery warning flag |

### Sample JSON State Payload

```json
{
  "battery": 93,
  "battery_low": false,
  "contact": true,
  "linkquality": 131,
  "tamper": false,
  "voltage": 2600
}
```

---

## Z2M Settings and Configuration

### Available Settings

The Settings tab in Z2M provides standard Zigbee device options:

| Setting | Description |
|---------|-------------|
| **debounce** | Debounces messages from this device |
| **debounce_ignore** | Protects unique payload values from overriding within debounce time |
| **disabled** | Disables the device (excludes from network scans, availability, and group state updates) |
| **filtered_attributes** | Filter attributes with regex from published payload |
| **filtered_cache** | Filter attributes from being added to cache |
| **filtered_optimistic** | Filter attributes from optimistic publish payload |

### Settings (Specific) Tab

For this sensor type, the "Settings (specific)" tab shows:
> **Empty exposes definition**

This indicates the sensor is a simple binary sensor with no device-specific configurable parameters beyond the standard Zigbee settings.

---

## Halachic Considerations

### Key Differences from Presence Sensors

Unlike mmWave/PIR presence sensors, door/window contact sensors have significant differences relevant to halachic analysis:

1. **Passive Detection**: The sensor doesn't actively scan - it only detects the magnetic field state
2. **Binary State**: Simple open/closed, no complex processing
3. **No Disable Option**: Cannot be "disabled" via software - the reed switch always responds to the magnet
4. **Direct Physical Causation**: Opening a door directly causes the sensor state change (not grama)

### The Core Question

When a person opens a door on Shabbat, and a contact sensor detects this:
- Is the person considered to have "done work" by changing an electrical state?
- Does it matter if the sensor change triggers an automation vs. simply being logged?
- Is the act of opening the door (permitted) separable from the sensor detection (potentially problematic)?

### Possible Approaches

1. **Disable Automations**: Keep sensor active but disable all Shabbat automations
2. **Physical Removal**: Remove sensor batteries before Shabbat
3. **Z2M Disable**: Use the "disabled" setting to exclude from network
4. **Accept Passive Monitoring**: If no actions are triggered, some may permit passive state logging

> **Important**: These are technical options only. Consult a qualified posek for halachic guidance.

---

## Z2M Screenshots Reference

The following screenshots from Zigbee2MQTT demonstrate the actual interface for this sensor:

1. **About Tab**: Device identification, model info (TS0203), battery status, MQTT topic
2. **Exposes Tab**: Contact state, battery %, voltage, tamper status, link quality
3. **Settings Tab**: Standard Zigbee device settings (debounce, disable, filter options)
4. **Settings (Specific)**: Empty - no device-specific settings available
5. **State Tab**: Raw JSON payload showing current sensor state

---

## Comparison: Door Sensor vs. Presence Sensor

| Aspect | Door/Window Sensor | Presence Sensor |
|--------|-------------------|-----------------|
| **Detection Method** | Magnetic reed switch | mmWave radar + PIR |
| **Active/Passive** | Passive | Active scanning |
| **Configurable Sensitivity** | No | Yes |
| **Can Be "Disabled" via Software** | Only via Z2M exclusion | Potentially via threshold settings |
| **Detection Trigger** | Physical movement of door | Human presence/motion |
| **Causation Type** | Direct | Potentially grama |
| **Battery Life** | 2+ years | Variable (depends on detection frequency) |

---

*This document is part of the Smart Home Halacha project exploring the intersection of home automation and Jewish law.*

*Generated: December 2024*
