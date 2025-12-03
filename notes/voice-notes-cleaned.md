# Voice Notes: Smart Home and Halacha

*Recorded: 3rd December 2025 (14th Kislev 5786)*

## Background: The Hebrew Date Widget

A side note to start: I'm particularly proud of my Hebrew date widget for KDE Plasma on Ubuntu. I was surprised to find that while there were Islamic and Nepali calendar widgets available, no one had created one for the Hebrew calendar. So I built one using the HebCal API, requiring geolocation (city-level precision is typically sufficient for Jewish calendar dates).

## Why This Repository Exists

I created this repository to gather notes on Jewish observance and smart home technology. I've previously shared templates for Home Assistant, including integrations like the "Shabbat and Holidays Jewish Integration" which provides binary sensors for Yom Tov and Shabbat.

### My Downstream Sensor Innovation

One of my first successful Home Assistant creations was a downstream sensor that combines Shabbat and Yom Tov into a single binary sensor. This is useful because many automations should trigger when *either* condition is true, rather than requiring separate trigger conditions.

## The Value of Smart Home for Observant Jews

Smart home technology offers enormous benefits for the religiously observant population:

- Replaces clunky old manual timers
- Zmanim sensors and Shabbat times work reliably
- No need to manually update timers on every device each week
- True "set it and forget it" automation

### Our Current Shabbat Automations

We've been running Shabbat automations based on the Hebrew calendar sensor:

- **30 minutes before Shabbat**: Speaker announcement, lighting preset activates
- **Midnight**: Bedtime automation (turns off AC in living room)
- **9:00 AM**: Morning automation (turns AC back on, etc.)
- **Afternoon**: Additional scene changes

These automations handle lights and ACs without any manual intervention. The Shabbat time sensor means you never need to update times manually - they come from the integration.

## Halachic Challenges to Explore

*Disclaimer: I am not a rabbi. These are open-source notes for exploration, not psak halacha.*

### Challenge 1: Human Presence Sensors

I recently set up human presence sensors (miniature radar-based motion detectors). They work brilliantly during the week:

**Current automation (midnight to 8 AM):**
- If no motion detected: lights turn off
- If motion detected: low light turns on (for midnight snack runs)
- When motion stops: lights turn off again

**The Shabbat Problem:**

The sensor registers motion regardless of whether automations act on it. Even if I add a condition `Shabbat == false` to prevent lights from activating, the sensor itself is still registering motion internally (going from false to true).

**Technical fix available:** Add Shabbat condition to automations - easy.

**Unresolved issue:** The sensor itself still registers state changes. Pulling batteries before Shabbat isn't practical with multiple sensors throughout the house.

### Challenge 2: Door/Window Security Sensors

These magnetic contact sensors are essential for our DIY alarm system (as renters without a professionally installed system):

**How they work:**
- Two small devices (~5cm each) with magnets
- One fixed to door frame, one to door
- When door opens, magnets separate, triggering a "true" condition
- Low power (battery lasts ~1 year), binary output only

**The Shabbat Problem:**

Similar to presence sensors - even if the alarm system is disarmed for Shabbat:
- Every door opening still triggers the sensor
- A small indicator light activates
- State changes are registered
- Guests leaving on Shabbat morning would trigger these conditions

**Why this matters more:** Security is a genuine need, not a luxury feature. It seems problematic to be unable to secure one's home, especially when this DIY approach may be the only option for renters.

## Questions for Further Research

1. Are there sensors specifically designed for the observant Jewish market that address these concerns?
2. What is the halachic status of passive state changes in sensors when no action results?
3. Does the security necessity (pikuach nefesh considerations) affect the analysis for alarm sensors?
4. Are there any workarounds beyond physically removing batteries?

## Notes

- Some organizations are involved in this space (names to be researched)
- This is a placeholder for ongoing exploration
- Will revisit and expand these notes over time
