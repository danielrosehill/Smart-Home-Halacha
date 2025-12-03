# Human Presence Sensors: Halachic Considerations

## What Are Human Presence Sensors?

Human presence sensors (also called mmWave or radar presence sensors) are small devices that detect human movement and presence using radar technology. Unlike PIR (passive infrared) motion sensors, they can detect even small movements like breathing.

### Technical Details

- **Technology**: Miniature radar (typically 24GHz mmWave)
- **Output**: Binary sensor (true/false for presence detected)
- **Features**: Configurable sensitivity threshold and cooldown time
- **Power**: Battery or USB powered
- **Integration**: Typically Zigbee, Z-Wave, or WiFi

### Reference Hardware: Tuya 24G mmWave + PIR Combo Sensor (~$13 USD)

This is a representative example of affordable presence sensors commonly available on AliExpress and similar platforms. The technical specifications are surprisingly sophisticated for the price point:

**Detection System (Dual-Mode)**:
- **24GHz mmWave Radar**: Static detection up to 3.5m, adjustable sensitivity (1-8x)
- **PIR Motion Sensor**: Motion detection up to 5m, fixed sensitivity
- **Operating Logic**: PIR triggers first; mmWave radar only activates once PIR detects someone, then monitors for continued presence (even stationary)

**Additional Sensors**:
- **Illuminance**: 0-3500 Lux range, sampled every 1 minute, reports on change
- **Temperature**: Sampled every 15 seconds, reports on 0.3°C change
- **Humidity**: Sampled every 15 seconds, reports on 3% change

**Power & Communication**:
- Battery: 2x AAA (DC 3V) or USB (DC 5V)
- Quiescent current: <65μA (very low power)
- Protocol: Zigbee 3.0 (requires gateway)
- Compatible with: Tuya/Smart Life app, Zigbee2MQTT

**Key Technical Note**: The "Presence Keep Time" parameter (adjustable, recommended 60+ seconds) determines how long the sensor maintains "presence detected" state after last movement. This is relevant because it affects how frequently state changes are transmitted.

*Full specifications: [sensors/presence/spec.txt](../sensors/presence/spec.txt)*

## The Use Case

**Weekday automation example:**

```yaml
# Between midnight and 8am:
# - No motion: lights off
# - Motion detected: dim light on (for midnight snack runs)
# - Motion stops: lights off again
```

This saves energy and provides convenience without manual intervention.

## The Shabbat Problem

### Level 1: Automation Triggers (Solvable)

Adding a condition to automations is straightforward:

```yaml
condition:
  - condition: state
    entity_id: binary_sensor.shabbat
    state: 'off'
```

This prevents the automation from executing on Shabbat, even if the sensor detects motion.

### Level 2: Sensor State Changes (Unsolved)

Even with automations disabled, the sensor itself:

1. **Detects motion** - the radar is always active
2. **Changes internal state** - from "no presence" to "presence detected"
3. **Transmits the state change** - via Zigbee/WiFi to the hub
4. **Logs the event** - in Home Assistant's database
5. **May illuminate an indicator LED** - showing state change

**The question**: Is triggering these internal state changes problematic on Shabbat, even when no visible action results?

### Level 3: Technical Details That Affect the Analysis

Based on the reference hardware specifications, several technical details are halachically relevant:

**1. Dual-Stage Detection (PIR → mmWave)**

The sensor's operating logic is: "When the current status is 'no one', the sensor detects presence through PIR, and only when PIR detects someone will it activate millimeter wave radar for static detection."

This means:
- Walking past the sensor triggers PIR (passive infrared)
- PIR detection then *activates* the mmWave radar
- mmWave radar monitors for continued presence

**Halachic implication**: The person's movement doesn't just cause a state change—it causes activation of additional circuitry (the mmWave radar). This may be more significant than a simple state toggle.

**2. Periodic Data Transmission**

The sensor actively transmits data on schedules:
- Light values: every 1 minute (if changed)
- Temperature/humidity: every 15 seconds (if thresholds exceeded)
- Presence state: on change

**Halachic implication**: Even if a person were to remain completely still, the environmental sensors are periodically transmitting. However, the *presence sensor* only transmits on state changes caused by human action.

**3. "Presence Keep Time" Parameter**

If set to 60+ seconds, the sensor maintains "presence detected" for that duration after last movement, reducing transmission frequency.

**Halachic implication**: Longer keep times mean fewer state changes per person passing through, but do not eliminate them.

**4. Power Draw Changes**

Quiescent current is <65μA, but active detection draws more. A person triggering detection causes increased current flow.

**Halachic implication**: Beyond state changes, there's a measurable physical change in electrical current caused by the person's presence.

## Potential Workarounds

### Option 1: Physical Disconnection (Impractical)

Remove batteries before Shabbat, replace after. Not viable with multiple sensors throughout the home.

### Option 2: Smart Plug Control (Partial)

For USB-powered sensors, connect to a smart plug that turns off before Shabbat. However:
- Requires additional hardware
- Doesn't work for battery-powered sensors
- The smart plug turning off is itself an action

### Option 3: Sensor "Sleep Mode" (If Available)

Some sensors may have a sleep or disable mode accessible via software. This could potentially be automated to engage before Shabbat.

### Option 4: Accept the State Changes

If the halachic conclusion is that passive electronic state changes without resulting action are permissible, no technical solution is needed.

## Questions for Rabbinic Consultation

### Core Questions

1. Is a radar sensor detecting presence analogous to being seen by a security camera (generally considered permissible)?

2. Does the electronic state change (false → true) constitute a form of "writing" or "building"?

3. Is this pesik reisha (inevitable consequence) if walking through one's home unavoidably triggers sensors?

4. Does davar she'eino mitkaven (unintended action) apply when the person has no interest in triggering the sensor?

5. If the sensor is primarily for weekday convenience (not necessity), does that affect the analysis?

### Technical-Specific Questions (Based on Hardware Specs)

6. **PIR → mmWave activation**: The sensor's dual-stage design means human motion causes the PIR to activate the mmWave radar circuit. Is activating dormant circuitry more significant than a simple state toggle? Does this resemble "building" a circuit?

7. **Radio transmission**: Each state change triggers a Zigbee transmission (radio waves). Is causing RF transmission different from causing an internal state change?

8. **Current draw changes**: Detection increases electrical current flow from <65μA to active levels. Does causing measurable physical changes in current constitute a problem?

9. **Comparison to existing technologies**: How does this compare to:
   - Walking in front of a security camera (optical detection)
   - Passing through automatic doors at a hospital (explicitly permitted for pikuach nefesh contexts)
   - Being detected by a neighbor's motion-activated outdoor light (triggering someone else's property)

10. **Sensor vs. automation distinction**: If the automation is disabled but the sensor still operates, does the halachic analysis differ from a sensor that actively triggers a light?

## Status

**Technical fix**: Available (condition-based automation disabling)

**Halachic question**: Open - regarding the sensor's internal state changes

## Notes

- These sensors are a "luxury" convenience item, not essential
- Original purpose was for a newborn's room - turning on dim light during nighttime diaper changes
- The same question applies to any motion-detecting sensor
