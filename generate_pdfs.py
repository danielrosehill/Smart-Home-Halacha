#!/usr/bin/env python3
"""
Generate PDF documentation for Smart Home Halacha sensor specifications.
Includes embedded images from AliExpress and Z2M screenshots.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib import colors
from pathlib import Path
import os

# Base paths
BASE_DIR = Path(__file__).parent
PRESENCE_DIR = BASE_DIR / "sensors" / "presence"
DOOR_DIR = BASE_DIR / "sensors" / "door"
OUTPUT_DIR = BASE_DIR / "output"

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

def get_styles():
    """Create custom styles for the PDF."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='Title1',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        textColor=HexColor('#1a365d')
    ))

    styles.add(ParagraphStyle(
        name='Title2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
        textColor=HexColor('#2c5282')
    ))

    styles.add(ParagraphStyle(
        name='Title3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
        textColor=HexColor('#2b6cb0')
    ))

    styles.add(ParagraphStyle(
        name='BodyText2',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        spaceBefore=6,
        spaceAfter=6,
        textColor=HexColor('#c53030'),
        borderColor=HexColor('#fc8181'),
        borderWidth=1,
        borderPadding=6,
        backColor=HexColor('#fff5f5')
    ))

    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        spaceBefore=4,
        spaceAfter=4,
        backColor=HexColor('#f7fafc'),
        borderColor=HexColor('#e2e8f0'),
        borderWidth=1,
        borderPadding=6
    ))

    styles.add(ParagraphStyle(
        name='Caption',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#718096'),
        alignment=1,  # Center
        spaceBefore=4,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor('#a0aec0'),
        alignment=1
    ))

    return styles


def create_table(data, col_widths=None):
    """Create a styled table."""
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#edf2f7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2d3748')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return table


def add_image(path, width=None, caption=None, styles=None, max_height=None):
    """Add an image with optional caption, properly scaled."""
    elements = []
    if path.exists():
        if width is None:
            width = 5.5 * inch
        if max_height is None:
            max_height = 4 * inch

        # Create image and get its natural size
        img = Image(str(path))
        iw, ih = img.wrap(0, 0)

        # Calculate aspect ratio
        aspect = ih / iw if iw > 0 else 1

        # Calculate dimensions while maintaining aspect ratio
        new_width = width
        new_height = width * aspect

        # If height exceeds max, scale down based on height
        if new_height > max_height:
            new_height = max_height
            new_width = max_height / aspect

        img = Image(str(path), width=new_width, height=new_height)
        img.hAlign = 'CENTER'
        elements.append(img)
        if caption and styles:
            elements.append(Paragraph(caption, styles['Caption']))
    return elements


def generate_presence_sensor_pdf():
    """Generate PDF for the presence sensor."""
    styles = get_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / "presence-sensor-specification.pdf"),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    story = []

    # Title
    story.append(Paragraph("24G MmWave Radar Human Presence Sensor", styles['Title1']))
    story.append(Paragraph("Smart Home Halacha Project - Hardware Documentation", styles['BodyText2']))
    story.append(Spacer(1, 20))

    # Overview
    story.append(Paragraph("Overview", styles['Title2']))
    story.append(Paragraph(
        "This document provides technical specifications and Zigbee2MQTT (Z2M) configuration details "
        "for the <b>Tuya ZG-204ZM</b> 24G MmWave Radar Human Presence Sensor, commonly available on "
        "AliExpress and similar platforms.",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 10))

    # AliExpress Images
    story.append(Paragraph("Product Images (AliExpress Samples)", styles['Title2']))
    story.append(Paragraph(
        "<i>Note: These images are representative examples from AliExpress listings. "
        "Actual products may vary by seller.</i>",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 10))

    # Add AliExpress images
    ali_img1 = PRESENCE_DIR / "1.png"
    ali_img2 = PRESENCE_DIR / "2.png"

    story.extend(add_image(ali_img1, 5*inch, "AliExpress listing showing 24G MmWave sensor with features", styles))
    story.extend(add_image(ali_img2, 4*inch, "Product features: 24G Radar, PIR, Luminance, Temperature, Humidity", styles))

    story.append(PageBreak())

    # Technical Specifications
    story.append(Paragraph("Technical Specifications", styles['Title2']))

    spec_data = [
        ['Parameter', 'Value'],
        ['Sensor Type A', '24G Radar + PIR + Luminance + Temperature + Humidity'],
        ['Sensor Type B', '24G Radar + PIR + Luminance'],
        ['Working Voltage', 'DC 3V'],
        ['Power Adapter', 'USB DC 5V'],
        ['Quiescent Current', '< 65uA'],
        ['Wireless Protocol', 'Zigbee 3.0 (requires Zigbee gateway)'],
        ['App Support', 'Smart Life / Tuya'],
        ['Illuminance Range', '0-3500 Lux'],
        ['Battery Type', '2x LR03 AAA (not included)'],
        ['Working Temperature', '-10C to 55C'],
        ['Working Humidity', 'max 95% RH'],
    ]
    story.append(create_table(spec_data, [2*inch, 4.5*inch]))
    story.append(Spacer(1, 15))

    # Detection Capabilities
    story.append(Paragraph("Detection Capabilities", styles['Title3']))
    detect_data = [
        ['Detection Type', 'Range', 'Notes'],
        ['Static Detection (Radar)', 'Max 3.5 meters', 'Sensitivity adjustable'],
        ['Motion Detection (PIR)', 'Max 5 meters', 'Fixed sensitivity'],
        ['Light Value Updates', 'Every 1 minute', 'On change only'],
        ['Temp/Humidity Updates', 'Every 15 seconds', '0.3C or 3% RH threshold'],
    ]
    story.append(create_table(detect_data, [1.8*inch, 1.5*inch, 3.2*inch]))
    story.append(Spacer(1, 15))

    # Operating Notes
    story.append(Paragraph("Important Operating Notes", styles['Title3']))
    notes = [
        "Zigbee devices must be connected to a Zigbee gateway to function",
        "After installation, align the sensing surface with the detection area",
        "For frequent false negatives, set 'Presence Keep Time' to 60+ seconds and sensitivity to 8x",
        "Low-power device - settings update only when device uploads data or is triggered",
        "When no presence detected, PIR activates first, then triggers mmWave radar for static detection"
    ]
    for i, note in enumerate(notes, 1):
        story.append(Paragraph(f"{i}. {note}", styles['BodyText2']))

    story.append(PageBreak())

    # Z2M Integration
    story.append(Paragraph("Zigbee2MQTT Integration", styles['Title2']))

    # Device ID table
    story.append(Paragraph("Device Identification", styles['Title3']))
    id_data = [
        ['Field', 'Value'],
        ['Zigbee Model', 'ZG-204ZM'],
        ['Manufacturer', 'HOBEIAN (PIR 24Ghz human presence sensor)'],
        ['Model', 'ZG-204ZM (Tuya)'],
        ['MQTT Topic', 'zigbee2mqtt/[device_name]'],
    ]
    story.append(create_table(id_data, [1.5*inch, 5*inch]))
    story.append(Spacer(1, 15))

    # Z2M Screenshots
    story.append(Paragraph("Z2M Interface Screenshots", styles['Title3']))

    z2m_images = [
        (PRESENCE_DIR / "z2m" / "1.png", "About Tab: Device identification and MQTT topic"),
        (PRESENCE_DIR / "z2m" / "2.png", "Exposes Tab: Presence, motion state, illuminance, and configurable parameters"),
    ]

    for img_path, caption in z2m_images:
        story.extend(add_image(img_path, 5.5*inch, caption, styles))

    story.append(PageBreak())

    # More Z2M screenshots
    z2m_images2 = [
        (PRESENCE_DIR / "z2m" / "3.png", "Exposes Tab (continued): Detection mode options - can toggle PIR/radar but not disable"),
        (PRESENCE_DIR / "z2m" / "params.png", "Full parameters view showing all configurable settings"),
    ]

    for img_path, caption in z2m_images2:
        story.extend(add_image(img_path, 5.5*inch, caption, styles))

    story.append(PageBreak())

    # More Z2M screenshots
    z2m_images3 = [
        (PRESENCE_DIR / "z2m" / "5.png", "Settings Tab: Device-level settings including disable option"),
        (PRESENCE_DIR / "z2m" / "6.png", "State Tab: JSON payload showing sensor state and parameters"),
    ]

    for img_path, caption in z2m_images3:
        story.extend(add_image(img_path, 5.5*inch, caption, styles))

    story.append(PageBreak())

    # Configurable Parameters
    story.append(Paragraph("Configurable Parameters", styles['Title2']))

    param_data = [
        ['Parameter', 'Range', 'Unit', 'Description'],
        ['Fading Time', '0-28800', 'seconds', 'Presence keep time'],
        ['Static Detection Distance', '0-6', 'meters', 'Radar detection range'],
        ['Static Detection Sensitivity', '0-10', 'x', 'Radar sensitivity multiplier'],
        ['Indicator', 'OFF/ON', '-', 'LED indicator mode'],
        ['Motion Detection Mode', 'only_pir / pir_and_radar / only_radar', '-', 'Detection method'],
        ['Motion Detection Sensitivity', '0-10', 'x', 'PIR/motion sensitivity'],
    ]
    story.append(create_table(param_data, [1.8*inch, 1.2*inch, 0.6*inch, 2.9*inch]))
    story.append(Spacer(1, 15))

    # Sample JSON
    story.append(Paragraph("Sample JSON State Payload", styles['Title3']))
    json_text = '''{
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
}'''
    story.append(Paragraph(f"<font face='Courier' size='8'>{json_text}</font>", styles['CodeBlock']))

    story.append(PageBreak())

    # Shabbat Solution
    story.append(Paragraph("Potential Shabbat Solution: Sensitivity Threshold Workaround", styles['Title2']))

    story.append(Paragraph(
        "<b>Disclaimer:</b> This is a theoretical technical approach only. It has NOT been tested to confirm "
        "effectiveness, and no halachic determination has been made regarding whether this approach is "
        "permissible or advisable. Consult with a qualified posek before implementing any Shabbat "
        "automation strategy.",
        styles['Disclaimer']
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("The Concept", styles['Title3']))
    story.append(Paragraph(
        "Since this sensor does not have a true 'disable' option, one potential workaround is to set "
        "the detection thresholds to values that would effectively prevent any detection from occurring.",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Key Observation:</b> The Z2M interface allows toggling between PIR and radar modes, "
        "but does NOT provide an option to disable detection entirely.",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 10))

    # Add the annotated screenshot showing the concept
    story.extend(add_image(
        PRESENCE_DIR / "z2m" / "4.png",
        5.5*inch,
        "Annotated screenshot showing potential Shabbat solution: configure thresholds that won't be met",
        styles
    ))

    story.append(Paragraph("Proposed Settings (Pre-Shabbat)", styles['Title3']))
    settings_data = [
        ['Parameter', 'Normal Value', 'Shabbat Value', 'Effect'],
        ['Static Detection Distance', '3-6 m', '0 m', "Radar won't detect at any distance"],
        ['Static Detection Sensitivity', '5-8x', '0x', 'Radar sensitivity at minimum'],
        ['Motion Detection Sensitivity', '5-8x', '0x', 'PIR sensitivity at minimum'],
    ]
    story.append(create_table(settings_data, [1.8*inch, 1.2*inch, 1.2*inch, 2.3*inch]))
    story.append(Spacer(1, 15))

    # Automation Example
    story.append(Paragraph("Sample Home Assistant Automation", styles['Title3']))
    story.append(Paragraph("<i>UNTESTED - Conceptual only</i>", styles['BodyText2']))

    automation_yaml = '''automation:
  - alias: "Presence Sensor - Pre-Shabbat Disable"
    trigger:
      - platform: state
        entity_id: binary_sensor.shabbat
        to: 'on'
    action:
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_presence/set"
          payload: |
            {"static_detection_distance": 0,
             "static_detection_sensitivity": 0,
             "motion_detection_sensitivity": 0}

  - alias: "Presence Sensor - Post-Shabbat Enable"
    trigger:
      - platform: state
        entity_id: binary_sensor.shabbat
        to: 'off'
    action:
      - service: mqtt.publish
        data:
          topic: "zigbee2mqtt/living_room_presence/set"
          payload: |
            {"static_detection_distance": 4,
             "static_detection_sensitivity": 6,
             "motion_detection_sensitivity": 6}'''

    story.append(Paragraph(f"<font face='Courier' size='7'>{automation_yaml}</font>", styles['CodeBlock']))

    story.append(PageBreak())

    # Critical Unknowns
    story.append(Paragraph("Critical Unknowns", styles['Title2']))

    story.append(Paragraph("Technical Questions (Require Testing)", styles['Title3']))
    tech_questions = [
        "Does sensitivity=0 actually prevent detection?",
        "Does distance=0 work as expected?",
        "What about the PIR sensor at minimum sensitivity?",
        "Do settings persist across power cycles?",
        "Is there latency in applying settings?"
    ]
    for q in tech_questions:
        story.append(Paragraph(f"- {q}", styles['BodyText2']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Halachic Questions (Require Rabbinic Consultation)", styles['Title3']))
    halachic_questions = [
        "Is 'effectively disabled' sufficient?",
        "What if the settings don't fully prevent detection?",
        "Is pre-Shabbat automation problematic?",
        "Grama considerations if sensor is 'armed' at 0 sensitivity"
    ]
    for q in halachic_questions:
        story.append(Paragraph(f"- {q}", styles['BodyText2']))
    story.append(Spacer(1, 15))

    # Alternative Approaches
    story.append(Paragraph("Alternative Approaches", styles['Title3']))
    alternatives = [
        "<b>Physical switch:</b> Install on USB power supply for manual disconnect before Shabbat",
        "<b>Removable batteries:</b> Remove before Shabbat (impractical for multiple sensors)",
        "<b>Disable automations only:</b> If sensor state changes without resulting actions are permissible"
    ]
    for alt in alternatives:
        story.append(Paragraph(f"- {alt}", styles['BodyText2']))

    story.append(Spacer(1, 30))

    # Footer
    story.append(Paragraph(
        "This document is part of the Smart Home Halacha project exploring the intersection "
        "of home automation and Jewish law.",
        styles['Footer']
    ))
    story.append(Paragraph("Generated: December 2024", styles['Footer']))

    doc.build(story)
    print(f"Generated: {OUTPUT_DIR / 'presence-sensor-specification.pdf'}")


def generate_door_sensor_pdf():
    """Generate PDF for the door/window sensor."""
    styles = get_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / "door-window-sensor-specification.pdf"),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    story = []

    # Title
    story.append(Paragraph("Door/Window Contact Sensor (Intrusion Sensor)", styles['Title1']))
    story.append(Paragraph("Smart Home Halacha Project - Hardware Documentation", styles['BodyText2']))
    story.append(Spacer(1, 20))

    # Overview
    story.append(Paragraph("Overview", styles['Title2']))
    story.append(Paragraph(
        "This document provides technical specifications and Zigbee2MQTT (Z2M) configuration details "
        "for <b>Zigbee door/window contact sensors</b>, commonly used for intrusion detection in smart "
        "home setups. The examples shown include the popular <b>Aqara MCCGQ11LM</b> and similar "
        "<b>Tuya TS0203</b> models.",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 10))

    # AliExpress Images
    story.append(Paragraph("Product Images (AliExpress Samples)", styles['Title2']))
    story.append(Paragraph(
        "<i>Note: These images are representative examples from AliExpress listings. "
        "Actual products may vary by seller.</i>",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 10))

    # Add AliExpress images
    story.extend(add_image(DOOR_DIR / "1.png", 4.5*inch, "Aqara door/window sensors - works with Mi Home and Apple HomeKit", styles))
    story.extend(add_image(DOOR_DIR / "2.png", 4.5*inch, "Low-Profile Mini Design: No Wiring, Installation Free, 2-Year Battery Life", styles))

    story.append(PageBreak())

    # Technical Specifications
    story.append(Paragraph("Technical Specifications", styles['Title2']))

    story.append(Paragraph("Aqara MCCGQ11LM", styles['Title3']))
    spec_data = [
        ['Parameter', 'Value'],
        ['Model', 'MCCGQ11LM'],
        ['Battery', 'CR1632 (included)'],
        ['Wireless Protocol', 'Zigbee'],
        ['Dimensions', '41 x 22 x 11 mm (1.61 x 0.87 x 0.43 in.)'],
        ['Maximum Detection Distance', '22 mm'],
        ['Operating Temperature', '-10C to +45C (14F to 113F)'],
        ['Operating Humidity', '0-95% RH, non-condensing'],
        ['App Support', 'Apple Home (iOS 10.3+), Aqara Home, Mi Home'],
    ]
    story.append(create_table(spec_data, [2*inch, 4.5*inch]))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Tuya TS0203 (Alternative)", styles['Title3']))
    tuya_data = [
        ['Parameter', 'Value'],
        ['Zigbee Model', 'TS0203'],
        ['Manufacturer', '_TZ3000_oxslv1c9'],
        ['Type', 'Door/window sensor'],
        ['Protocol', 'Zigbee 3.0'],
    ]
    story.append(create_table(tuya_data, [2*inch, 4.5*inch]))
    story.append(Spacer(1, 20))

    # Operating Principle
    story.append(Paragraph("Operating Principle", styles['Title2']))
    story.append(Paragraph(
        "Door/window contact sensors use a <b>magnetic reed switch</b> mechanism:",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 6))

    principles = [
        "<b>Main Unit:</b> Contains the reed switch and Zigbee radio",
        "<b>Magnet:</b> Small magnetic piece attached to the moving part (door/window)",
        "<b>Detection:</b> When magnet is near (door closed), circuit is closed; when separated (door open), circuit opens",
        "<b>Detection Distance:</b> Typically 15-22mm maximum gap for reliable detection"
    ]
    for p in principles:
        story.append(Paragraph(f"- {p}", styles['BodyText2']))
    story.append(Spacer(1, 10))

    # Sensor States
    story.append(Paragraph("Sensor States", styles['Title3']))
    state_data = [
        ['Physical State', 'Sensor Reading', 'Contact Value'],
        ['Door/Window Closed', 'Magnet Near', 'true (Closed)'],
        ['Door/Window Open', 'Magnet Far', 'false (Open)'],
    ]
    story.append(create_table(state_data, [2*inch, 2*inch, 2.5*inch]))

    story.append(PageBreak())

    # Z2M Integration
    story.append(Paragraph("Zigbee2MQTT Integration", styles['Title2']))

    # Device ID table
    story.append(Paragraph("Device Identification (Tuya TS0203)", styles['Title3']))
    id_data = [
        ['Field', 'Value'],
        ['Zigbee Model', 'TS0203'],
        ['Description', 'Door/window sensor'],
        ['Manufacturer', 'Tuya'],
        ['MQTT Topic', 'zigbee2mqtt/[device_name]'],
        ['Support Status', 'Supported: native'],
    ]
    story.append(create_table(id_data, [1.5*inch, 5*inch]))
    story.append(Spacer(1, 15))

    # Exposed Parameters
    story.append(Paragraph("Exposed Parameters", styles['Title3']))
    param_data = [
        ['Parameter', 'Type', 'Description'],
        ['Contact', 'Boolean', 'Indicates if contact is closed (true) or open (false)'],
        ['Battery', 'Percentage', 'Remaining battery (may take up to 24 hours to report)'],
        ['Voltage', 'Integer (mV)', 'Battery voltage in millivolts'],
        ['Tamper', 'Boolean', 'Indicates if device has been tampered with'],
        ['Link Quality', 'Integer (lqi)', 'Zigbee signal strength'],
        ['Battery Low', 'Boolean', 'Low battery warning flag'],
    ]
    story.append(create_table(param_data, [1.3*inch, 1.3*inch, 3.9*inch]))
    story.append(Spacer(1, 15))

    # Sample JSON
    story.append(Paragraph("Sample JSON State Payload", styles['Title3']))
    json_text = '''{
  "battery": 93,
  "battery_low": false,
  "contact": true,
  "linkquality": 131,
  "tamper": false,
  "voltage": 2600
}'''
    story.append(Paragraph(f"<font face='Courier' size='8'>{json_text}</font>", styles['CodeBlock']))

    story.append(PageBreak())

    # Z2M Screenshots
    story.append(Paragraph("Z2M Interface Screenshots", styles['Title2']))

    z2m_images = [
        (DOOR_DIR / "z2m" / "2.png", "About Tab: Device identification (TS0203), battery status, MQTT topic"),
        (DOOR_DIR / "z2m" / "3.png", "Exposes Tab: Contact state, battery %, voltage, tamper status, link quality"),
    ]

    for img_path, caption in z2m_images:
        story.extend(add_image(img_path, 5.5*inch, caption, styles))

    story.append(PageBreak())

    # More Z2M screenshots
    z2m_images2 = [
        (DOOR_DIR / "z2m" / "1.png", "Settings Tab: Standard Zigbee device settings (debounce, disable, filter options)"),
        (DOOR_DIR / "z2m" / "4.png", "Settings (Specific): Empty - no device-specific settings available"),
    ]

    for img_path, caption in z2m_images2:
        story.extend(add_image(img_path, 5.5*inch, caption, styles))

    story.extend(add_image(DOOR_DIR / "z2m" / "5.png", 5*inch, "State Tab: Raw JSON payload showing current sensor state", styles))

    story.append(PageBreak())

    # Halachic Considerations
    story.append(Paragraph("Halachic Considerations", styles['Title2']))

    story.append(Paragraph("Key Differences from Presence Sensors", styles['Title3']))
    story.append(Paragraph(
        "Unlike mmWave/PIR presence sensors, door/window contact sensors have significant differences "
        "relevant to halachic analysis:",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 6))

    differences = [
        "<b>Passive Detection:</b> The sensor doesn't actively scan - it only detects the magnetic field state",
        "<b>Binary State:</b> Simple open/closed, no complex processing",
        "<b>No Disable Option:</b> Cannot be 'disabled' via software - the reed switch always responds to the magnet",
        "<b>Direct Physical Causation:</b> Opening a door directly causes the sensor state change (not grama)"
    ]
    for d in differences:
        story.append(Paragraph(f"- {d}", styles['BodyText2']))
    story.append(Spacer(1, 15))

    story.append(Paragraph("The Core Question", styles['Title3']))
    story.append(Paragraph(
        "When a person opens a door on Shabbat, and a contact sensor detects this:",
        styles['BodyText2']
    ))
    questions = [
        "Is the person considered to have 'done work' by changing an electrical state?",
        "Does it matter if the sensor change triggers an automation vs. simply being logged?",
        "Is the act of opening the door (permitted) separable from the sensor detection (potentially problematic)?"
    ]
    for q in questions:
        story.append(Paragraph(f"- {q}", styles['BodyText2']))
    story.append(Spacer(1, 15))

    # Possible Approaches
    story.append(Paragraph("Possible Approaches", styles['Title3']))
    approaches = [
        "<b>Disable Automations:</b> Keep sensor active but disable all Shabbat automations",
        "<b>Physical Removal:</b> Remove sensor batteries before Shabbat",
        "<b>Z2M Disable:</b> Use the 'disabled' setting to exclude from network",
        "<b>Accept Passive Monitoring:</b> If no actions are triggered, some may permit passive state logging"
    ]
    for a in approaches:
        story.append(Paragraph(f"- {a}", styles['BodyText2']))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Important:</b> These are technical options only. Consult a qualified posek for halachic guidance.",
        styles['Disclaimer']
    ))

    story.append(PageBreak())

    # Comparison Table
    story.append(Paragraph("Comparison: Door Sensor vs. Presence Sensor", styles['Title2']))

    compare_data = [
        ['Aspect', 'Door/Window Sensor', 'Presence Sensor'],
        ['Detection Method', 'Magnetic reed switch', 'mmWave radar + PIR'],
        ['Active/Passive', 'Passive', 'Active scanning'],
        ['Configurable Sensitivity', 'No', 'Yes'],
        ['Can Be "Disabled" via Software', 'Only via Z2M exclusion', 'Potentially via threshold settings'],
        ['Detection Trigger', 'Physical movement of door', 'Human presence/motion'],
        ['Causation Type', 'Direct', 'Potentially grama'],
        ['Battery Life', '2+ years', 'Variable'],
    ]
    story.append(create_table(compare_data, [2*inch, 2.25*inch, 2.25*inch]))

    story.append(Spacer(1, 30))

    # Footer
    story.append(Paragraph(
        "This document is part of the Smart Home Halacha project exploring the intersection "
        "of home automation and Jewish law.",
        styles['Footer']
    ))
    story.append(Paragraph("Generated: December 2024", styles['Footer']))

    doc.build(story)
    print(f"Generated: {OUTPUT_DIR / 'door-window-sensor-specification.pdf'}")


if __name__ == "__main__":
    print("Generating PDFs for Smart Home Halacha project...")
    generate_presence_sensor_pdf()
    generate_door_sensor_pdf()
    print("Done!")
