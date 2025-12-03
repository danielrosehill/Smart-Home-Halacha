# Smart Home + Halacha

This repository is a small collection of notes that I may update over time regarding questions of halacha that may arise in respect to smart home operation. 

Smart home technologies - like Home Assistant - offer enormous benefits and flexibility to religiously observant Jewish users. 

To that end, from time to time, I have shared a few notes and scripts - such as [this template](https://github.com/danielrosehill/Home-Assistant-YomTov-Shabbat-0125) which offers a downstream combined Shabbat and Yom Tov sensor so that automations can be triggered when *either* condition is true.

Home Assistant can be used to:

- Replace manual timers with smart ones that can be calibrated automatically to Shabbat times (thanks to the work of projects like HebCal and integrations like Jewish Calendar!) 
- Provide visual indications for the start and end of Shabbat and *hagim* (when Shabbat is over, turn this light off, etc)  

It's even helpful from an environmental and cost-saving standpoint.

Before HA:

- Leave air conditioning running for the whole of Shabbat/Chag

After HA:

- Set up a recurring Shabbat/Chag automation. Scenes and automations turn lighting and ACs on and off befitting a recurrent pattern. 

## Current Topics

### Sensor State Changes on Shabbat

The primary focus currently is on sensors that register state changes even when automations are disabled:

- **Human Presence Sensors**: Radar-based motion detection that registers movement internally
- **Door/Window Security Sensors**: Magnetic contact sensors that trigger on door opening

See the [notes/](notes/) directory for detailed exploration of these questions.

### Existing Resources

- [Combined Shabbat/Yom Tov Sensor Template](https://github.com/danielrosehill/Home-Assistant-YomTov-Shabbat-0125)

## Disclaimer

I am not a Rabbi! These are merely my own personal notes and may not be reflective of the halacha you hold by. Consult your posek for actual halachic guidance. 