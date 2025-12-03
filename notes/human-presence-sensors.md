# Human Presence Sensors: Halachic Considerations

## What Are Human Presence Sensors?

Human presence sensors (also called mmWave or radar presence sensors) are small devices that detect human movement and presence using radar technology. Unlike PIR (passive infrared) motion sensors, they can detect even small movements like breathing.

### Technical Details

- **Technology**: Miniature radar (typically 24GHz mmWave)
- **Output**: Binary sensor (true/false for presence detected)
- **Features**: Configurable sensitivity threshold and cooldown time
- **Power**: Battery or USB powered
- **Integration**: Typically Zigbee, Z-Wave, or WiFi

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

1. Is a radar sensor detecting presence analogous to being seen by a security camera (generally considered permissible)?

2. Does the electronic state change (false → true) constitute a form of "writing" or "building"?

3. Is this pesik reisha (inevitable consequence) if walking through one's home unavoidably triggers sensors?

4. Does davar she'eino mitkaven (unintended action) apply when the person has no interest in triggering the sensor?

5. If the sensor is primarily for weekday convenience (not necessity), does that affect the analysis?

## Status

**Technical fix**: Available (condition-based automation disabling)

**Halachic question**: Open - regarding the sensor's internal state changes

## Notes

- These sensors are a "luxury" convenience item, not essential
- Original purpose was for a newborn's room - turning on dim light during nighttime diaper changes
- The same question applies to any motion-detecting sensor
