# Potential Shabbat Solution: Sensitivity Threshold Workaround

> **Disclaimer**: This is a theoretical technical approach only. It has NOT been tested to confirm effectiveness, and no halachic determination has been made regarding whether this approach is permissible or advisable. Consult with a qualified posek before implementing any Shabbat automation strategy.

## The Idea

Since the Tuya ZG-204ZM presence sensor does not have a true "disable" option, one potential workaround is to set the detection thresholds to values that would effectively prevent any detection from occurring.

## Proposed Settings (Pre-Shabbat)

Based on the Z2M Exposes interface, the following settings could theoretically "disable" detection:

| Parameter | Normal Value | Shabbat Value | Effect |
|-----------|-------------|---------------|--------|
| **Static detection distance** | 3-6 m | **0 m** | Radar won't detect at any distance |
| **Static detection sensitivity** | 5-8x | **0x** | Radar sensitivity at minimum |
| **Motion detection sensitivity** | 5-8x | **0x** | PIR sensitivity at minimum |

## Automation Concept

A Home Assistant automation could adjust these values before and after Shabbat:

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

## Critical Unknowns

### Technical Questions (Require Testing)

1. **Does sensitivity=0 actually prevent detection?** The slider allows 0, but it may still detect at very close range or with large movements.

2. **Does distance=0 work as expected?** Setting distance to 0m might be ignored by the firmware, or it might have a minimum threshold.

3. **What about the PIR sensor?** The PIR (passive infrared) may not have as granular control. Even with motion_detection_sensitivity=0, it might still trigger on large movements.

4. **Do settings persist across power cycles?** If the sensor loses power briefly, do these settings reset to defaults?

5. **Is there latency in applying settings?** The automation would need to run with sufficient lead time before Shabbat.

### Halachic Questions (Require Rabbinic Consultation)

1. **Is "effectively disabled" sufficient?** Even if detection is practically impossible, the sensor circuitry is still active and attempting to detect. Is this halachically equivalent to being off?

2. **What if it fails?** If the settings don't fully prevent detection (e.g., someone stands very close), does the person bear responsibility for triggering the sensor?

3. **Pre-Shabbat automation**: Is having an automation change device settings before Shabbat problematic in any way?

4. **Grama considerations**: If the sensor is "armed" to potentially detect (even at 0 sensitivity), does walking past constitute grama (indirect causation)?

## Alternative Approaches

If the sensitivity workaround proves ineffective or halachically problematic:

1. **Physical switch**: Install a physical switch on the sensor's power supply (for USB-powered units) to manually disconnect before Shabbat.

2. **Removable batteries**: For battery-powered sensors, simply remove batteries before Shabbat (impractical for multiple sensors).

3. **Accept and disable automations only**: If the halachic conclusion is that sensor state changes without resulting actions are permissible, simply disable the automations and leave the sensor operating normally.

## Next Steps

1. **Test the sensitivity settings** to determine if 0/0/0 actually prevents detection
2. **Consult with a posek** regarding the halachic implications of this approach
3. **Document findings** for the broader community

---

*This document is part of the Smart Home Halacha project exploring the intersection of home automation and Jewish law.*
