# Door/Window Security Sensors: Halachic Considerations

## What Are Door/Window Contact Sensors?

Magnetic contact sensors (also called reed switches) detect when a door or window is opened. They're a fundamental component of both professional and DIY alarm systems.

### Technical Details

- **Technology**: Magnetic reed switch - two components with magnets
- **Installation**: One piece on door frame, one on door itself
- **Output**: Binary sensor (true = open/separated, false = closed/together)
- **Power**: Battery (typically lasts 1+ year)
- **Size**: Small (~4-5cm each piece)
- **Integration**: Zigbee, Z-Wave, or proprietary wireless

### Reference Hardware: Aqara Door/Window Sensor MCCGQ11LM (~$10-15 USD)

A representative example of a typical Zigbee contact sensor:

- **Model**: MCCGQ11LM
- **Battery**: CR1632 (included)
- **Protocol**: Zigbee 3.0
- **Dimensions**: 41 × 22 × 11 mm (very compact)
- **Detection Distance**: 22mm maximum gap between sensor and magnet
- **Operating Temperature**: -10°C to +45°C
- **Operating Humidity**: 0-95% RH (non-condensing)
- **Compatibility**: Apple HomeKit, Aqara Home, Mi Home, Zigbee2MQTT

*Full specifications: [sensors/door/spec.txt](../sensors/door/spec.txt)*

### How They Work

1. When door is closed, magnets are adjacent → sensor reports "closed" (false)
2. When door opens, magnets separate → sensor reports "open" (true)
3. Sensor may briefly illuminate an LED on state change
4. State change is transmitted to hub and logged

### Technical Contrast with Presence Sensors

Door/window sensors are mechanically simpler than presence sensors:

| Aspect | Door/Window Sensor | Presence Sensor |
|--------|-------------------|-----------------|
| Detection mechanism | Reed switch (magnetic) | PIR + mmWave radar |
| Active circuitry | Minimal - switch completes/breaks circuit | Complex - PIR triggers radar activation |
| Triggered by | Physical separation of components | Body heat + movement + presence |
| Power draw change | Negligible | Significant (radar activation) |
| Transmission | On state change only | State changes + periodic environmental data |

**Halachic implication**: The simpler mechanism of door sensors may be relevant. Opening a door causes a magnetic reed switch to change state — this is more mechanically direct than the multi-stage PIR→mmWave activation in presence sensors. However, both still result in Zigbee transmission and logging.

### Zigbee2MQTT Configuration Options

The Z2M interface for door/window sensors is notably simpler than presence sensors:

**Sensor Exposes (what the device reports)**:
- **Contact**: Boolean (true = closed, false = open) — the core state
- **Battery**: Percentage (can take up to 24 hours to update)
- **Voltage**: Battery voltage in millivolts (e.g., 2600 mV)
- **Tamper**: Boolean — indicates if device has been physically tampered with
- **Linkquality**: Signal strength (LQI value)

**State Payload (what gets transmitted)**:
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

**Z2M General Settings** (same as presence sensor):
- **disabled**: Excludes device from Z2M processing (sensor still operates)
- **debounce**: Rate-limits message processing
- **filtered_attributes**: Can suppress specific attributes from MQTT publishing

**Settings (specific) tab**: Empty — no device-specific configurable parameters exposed

**Key Differences from Presence Sensors**:

1. **No configurable detection parameters**: Unlike the presence sensor with its sensitivity sliders and detection modes, the door sensor has no user-adjustable settings. It simply reports open/closed.

2. **No way to reduce sensitivity**: You cannot configure the reed switch to be "less sensitive" — magnets either separate or they don't.

3. **Tamper detection**: The sensor includes tamper detection, which means physically covering/blocking it would trigger a different state change.

4. **Simpler payload**: Fewer attributes transmitted per state change.

**Halachically Relevant Observations**:

1. **No "Shabbat mode" possible at sensor level**: Unlike presence sensors where you might hack sensitivity settings, door sensors offer no configuration that could prevent detection.

2. **Z2M filtering is the only software option**: Using `filtered_attributes` to suppress `contact` from being published would prevent Home Assistant from seeing state changes — but the sensor still detects and transmits via Zigbee.

3. **Physical workaround possible but impractical**: Taping a small magnet to the door frame side could keep the reed switch "closed" regardless of door position — but this defeats the purpose entirely and is impractical for daily use.

4. **Tamper creates additional concern**: If someone tries to physically disable/cover the sensor, the tamper state would change — creating another human-triggered state change.

*Z2M screenshots: [sensors/door/z2m/](../sensors/door/z2m/)*

## The Use Case

**DIY Alarm System (especially for renters):**

For those who cannot install professional alarm systems (common for renters), door/window sensors provide essential security monitoring:

```yaml
# If any entry sensor changes to "open" between midnight and 6am
# and alarm is armed → trigger alert
```

Professional systems often use laser break-beam sensors, but DIY systems typically rely on magnetic contact sensors.

## The Shabbat Problem

### Level 1: Alarm Triggers (Solvable)

Disarming the alarm for Shabbat prevents notifications and alerts:

```yaml
condition:
  - condition: state
    entity_id: binary_sensor.shabbat
    state: 'off'
```

Or simply: don't arm the alarm system on Shabbat.

### Level 2: Sensor State Changes (Unsolved)

Even with the alarm disarmed, each time a door opens:

1. **Physical separation** occurs between the magnet components
2. **Reed switch activates** - electrical state changes
3. **Sensor transmits** state change to hub
4. **LED may illuminate** briefly
5. **Event is logged** in Home Assistant

**Scenario**: Shabbat guests leaving on Saturday morning trigger multiple door sensors as they exit, even though no alarm sounds.

## Why This Matters More Than Presence Sensors

### Security Is Not a Luxury

Unlike human presence sensors (which are convenience devices), security monitoring addresses a genuine need:

- Protection of home and family
- Especially relevant for renters without professional options
- May involve pikuach nefesh (life safety) considerations

### The Dilemma

Being unable to have *any* home security monitoring on Shabbat seems like a significant gap. But the sensors still register state changes even when "disarmed."

## Potential Considerations

### Pikuach Nefesh

If home security is genuinely necessary (high-crime area, known threats, etc.), does this override concerns about sensor state changes?

### Grama (Indirect Causation)

Opening a door is a normal activity. The sensor detecting this is:
- Not the person's intent
- An indirect result of a normal action
- Analogous to triggering automatic sliding doors?

### Comparison to Existing Rulings

How do poskim view:
- Security cameras on Shabbat (generally permissible to walk past)
- Automatic doors (various opinions)
- Motion-activated lights in public spaces (various opinions)

## Potential Workarounds

### Option 1: Accept Partial Security

Only arm sensors on windows (which shouldn't open on Shabbat anyway), leave door sensors passive.

### Option 2: Shabbat Mode for Hub

Some systems may support a complete "Shabbat mode" that stops processing sensor data entirely. The sensors would still transmit, but nothing would receive/log.

### Option 3: Physical Sensor Bypass

Small physical covers that prevent magnet separation - impractical for frequent door use.

### Option 4: Alternative Sensor Technology

Research whether any sensor types exist that don't transmit/log state changes while in a "passive" mode.

## Questions for Rabbinic Consultation

1. Does the security need (for renters without alternatives) affect the halachic analysis?

2. Is triggering a door sensor different from walking past a security camera?

3. When the alarm is disarmed and no action results, is the state change itself significant?

4. Could this be considered a permissible grama given that:
   - Opening the door is the intended action
   - The sensor triggering is incidental
   - No notification/alarm results

5. For windows that won't be opened on Shabbat anyway - are those sensors less problematic to leave active?

## Status

**Technical fix**: Available for alarm *response* (disarm on Shabbat)

**Halachic question**: Open - regarding:
- Sensor state changes when alarm is disarmed
- Whether security needs affect the analysis
- Comparison to other automatic detection systems

## Notes

- This is potentially more serious than the presence sensor question due to the security aspect
- Multiple sensors throughout home (10+ in typical setup)
- Affects both residents and Shabbat guests
- Professional alarm systems may have different mechanisms (laser-based) that present different halachic questions
