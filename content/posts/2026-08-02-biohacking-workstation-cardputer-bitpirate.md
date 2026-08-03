---
title: "A Biohacking Workstation in Your Pocket: Cardputer + BitPirate Against Embedded Medical Devices"
date: 2026-08-02
category: Engineering
tags: hardware hacking, medical devices, Cardputer, M5Stack, BitPirate, ESP32-S3, UART, I2C, SPI, JTAG, SWD, BLE, sub-GHz, CC1101, nRF24, firmware analysis, binwalk, Ghidra, infusion pump, medical device security, reverse engineering, biomedical engineering, right to repair
level: Advanced
read_time: 30 min
summary: "A single ESP32-S3 board the size of a business card, running open-source firmware, will speak nearly every wired bus and radio protocol an embedded medical device uses. This is how I use an M5Stack Cardputer ADV with BitPirate as a portable protocol workbench — to map hardware, watch a device boot, sniff its buses and radios, and pull its firmware — worked all the way through with an infusion pump, plus a targeted probing plan. Authorised, isolated, off the patient. The legal and safety constraints are not an appendix here; they are the first tool you pick up."
featured: false
---

<div style="font-size:0.9em; background:linear-gradient(135deg,#0f3d2e 0%,#14532d 100%); color:#eafff4; padding:1.2em 1.6em; border-radius:8px; margin:1.5em 0; line-height:1.6;">
🔬 <strong>A service for medical institutions.</strong> Alongside reverse-engineering obsolete mechanical parts back into service, I characterise the <em>electronics and protocols</em> of embedded medical devices — for repair, interoperability, data-integrity validation, and defensive security review. This post is the electronic sibling of my spare-parts work: instead of calipers and CAD, the bench tool is a keyboard-sized multi-protocol analyser. Everything below assumes an owned or explicitly authorised device, powered up in isolation, <strong>never connected to a patient or a live clinical network.</strong>
</div>

When I was a medical student at Kenyatta National Hospital I brought dead machines back to life — fuses in incubators, heating elements, thermostats, and, when I was brave enough, motherboards on CT scanners. I have written before about the mechanical half of that work: [measuring a broken part and reverse-engineering it into parametric CAD](/post/2026-07-25-reverse-engineering-medical-spare-parts) so a discontinued component can be printed and fitted. This post is about the other half — the half that lives on the bus and in the radio, where the device's real behaviour is written in bytes and timing rather than in plastic and metal.

As you read through this text, remember that I also provide this as a training course. So if you yourself or your staff need to be trained on how to hack machines and build parts using 3D printers to resurrect those dead machines, you can leverage what I know by getting me to train your staff and pass on my knowledge to them so that they can take over from me and run your biomedical departments. If this is something that you would like to avail yourself of, do get in touch. 

For years the electronic half needed a bench full of instruments: a bus analyser here, a JTAG probe there, a software-defined radio, a logic analyser, a fistful of adapters. What has changed is that a single ESP32-S3 board the size of a business card, running the right open-source firmware, now does a usable version of all of it. The one I carry is an **M5Stack Cardputer ADV** flashed with **[BitPirate](https://github.com/geo-tp/ESP32-Bit-Pirate)** (properly, *ESP32 Bit Pirate*). It is not a replacement for a proper lab. It is something arguably more useful: a competent, standalone, pocketable *first* instrument that tells you, in the first hour, what the device is and where the interesting seams are — so that if you then need to escalate to the heavier gear, you know exactly where to point it.

## Why this combination, specifically

Two things make the Cardputer/BitPirate pairing worth writing about rather than just another dev board.

The first is **BitPirate itself**. It is open-source firmware, inspired by the legendary Bus Pirate, that turns a supported ESP32-S3 board into a multi-protocol workbench driven by a single consistent CLI. The command grammar is uniform across every mode — you select a `mode`, ask for `help`, then `scan`, `sniff`, or issue mode-specific commands — and the same CLI is reachable three ways: over USB serial, over a Wi-Fi web CLI, and, on the Cardputer, **standalone** using the device's own keyboard and screen with no host computer at all. That last point is the one that matters at a hospital bench where you would rather not tether a laptop to a device you are still deciding is safe to touch.

The protocol coverage is genuinely broad. From the current firmware, the wired and radio modes include:

| Class | Modes BitPirate exposes |
|---|---|
| **Wired buses** | I²C (scan, glitch, slave, dump, EEPROM), SPI (EEPROM, flash, SD, slave), UART + half-duplex UART (bridge, read, write, baud auto-detect), 1-Wire (iButton, EEPROM), 2-Wire / 3-Wire (sniff, smartcard/SLE4442, EEPROM), CAN (sniff, send/receive frames), I²S |
| **Debug / programming** | JTAG (scan), SWD, OpenOCD flows; SPI-NOR flash read; AVR and STM32 bootloader/ST-Link workflows via the browser tools |
| **Digital I/O & signals** | DIO (read, pull-up, set), PWM/servo, SUMP-compatible logic capture |
| **USB** | CDC, HID, MSC, and USB host adapter modes |
| **Radio** | Wi-Fi (sniff, deauth, nmap, netcat), Bluetooth/BLE (scan, sniff, spoof, HID), Sub-GHz via CC1101 (analyse, record, replay), nRF24 (scan, send, receive), RFID (read, write, clone), infrared (record/replay, ~80 protocols), FM |
| **Automation** | Bus-Pirate-style bytecode scripting *and* Python scripting over serial |

That table is not a marketing list — it is a map of the attack and analysis surface of a modern embedded medical device, and the overlap is nearly total.

The second thing is the **Cardputer ADV** as the host board. The original Cardputer is charming but exposes only two GPIO on a single Grove connector, which throttles the wired-bus work badly. The **ADV** brings out **12 GPIO** across Grove *and* a header, plus a screen, a full keyboard, microphone, speaker, IR transmitter, SD card, an IMU, and a battery. Twelve pins is the difference between "I can watch one UART" and "I can sit on a SPI bus (SCK/MOSI/MISO/CS), share ground, and still have a spare line for a chip-select or a reset." For standalone bench work on real hardware, the ADV is the one to flash.

Two honest limitations to state up front, because they shape the whole workflow:

1. **Radio add-ons.** The Cardputer has Wi-Fi, BLE, and an IR transmitter on-board, but **Sub-GHz (CC1101) and nRF24 need external modules** wired to the bus, or a companion like the Expander / a board such as the T-Embed CC1101 that carries those radios natively. If your target's proprietary telemetry lives at 433/868/915 MHz, plan the hardware for it.
2. **Voltage.** The ESP32-S3 is a **3.3 V** part. Medical PCBs are frequently 3.3 V but not always, and a 5 V line on an ESP32 GPIO is how you turn a diagnostic session into a repair bill. Level-shifting and a multimeter are not optional.

And the most important framing of all: BitPirate does not "understand" HL7, DICOM, or IEEE 11073. It gets you down to the **raw bytes and timing on the physical and link layers** that carry those protocols. The clinical semantics are reconstructed afterwards, by you, offline. Keep that division of labour in mind — it is the whole reason the workflow below is structured the way it is.

## The instrument you pick up first is the law

I am going to be unusually blunt about this section because in medical work it is not a disclaimer, it is a design constraint that determines whether the rest of the post is legitimate engineering or something I would refuse to write.

**Before any probe touches any pin:**

- **Authorisation is in writing.** Ownership, a manufacturer research agreement, a documented right-to-repair basis, or an institutional review that names the device and the scope. "It was in the store room" is not authorisation. Circumventing access controls on a device you do not own or are not authorised to test is a crime in most jurisdictions, medical or not.
- **The device is off the patient and off the network.** Physically disconnected from any patient, and air-gapped from the clinical network. You are characterising a *specimen*, not intercepting *care*. This single rule eliminates the entire class of harms that make medical-device hacking newsworthy for the wrong reasons.
- **The device is a spare, a decommissioned unit, or a lab loaner** — never one that is in service or in a maintenance pool that could put it back into service without a full re-qualification.
- **Tamper and safety realities are respected.** Many medical devices have secure boot, signed firmware, tamper detection, and battery-backed intrusion switches. Probing can void warranties, trip locks, or brick a unit. Assume the manufacturer built the device to notice you.
- **Findings go through responsible disclosure.** If this is security work and you find something, it goes to the manufacturer and, where appropriate, to the relevant coordination body (in the US, that pathway runs through the FDA's pre/postmarket cybersecurity guidance and CISA/ICS-CERT advisories). You publish *after* a fix or an agreed timeline, not before, and never with a working exploit against a fielded device.

The firmware's own authors put a warning to this effect on the front page — "educational, diagnostic, and interoperability testing purposes only." Treat that as the first line of your lab notebook, not the fine print.

With that established, here is the workflow.

## The workflow, stage by stage

I run this as a funnel: cheap, non-invasive, reversible observations first; irreversible or higher-risk actions last, and only if justified by what the earlier stages revealed. On a medical device the funnel matters more than usual, because every stage down is a stage closer to something the manufacturer designed to resist.

### Stage 0 — Passive reconnaissance and documentation

Before opening anything, I build a paper (well, Markdown) trail: model and revision, FCC ID (which, looked up, often reveals radio chipsets, frequencies, and internal photos in the FCC filing — a free head start), service-manual availability, and the companion app or gateway if one exists. If there is a phone app, its BLE behaviour can be observed later and cross-referenced. The FCC internal photos alone frequently tell you the MCU family and the radio before you have removed a single screw.

### Stage 1 — Physical inspection and pinout mapping

Powered **off**, enclosure open (if authorised), PCB photographed at high resolution under raking light so silkscreen legends read cleanly. I am looking for:

- **Unpopulated headers** labelled `UART`, `TX/RX`, `JTAG`, `SWD`, `SWO`, `ISP`, `DEBUG`, or a bare row of 0.1"/1.27" pads near the MCU.
- **Test points** clustered around the MCU, the radio, flash chips, and connectors — these are the manufacturer's own debug and test access, and they are gold.
- **Chip markings**: MCU (STM32, Nordic nRF52, ESP32, NXP Kinetis, TI MSP430…), radio, external SPI/I²C flash and EEPROM, sensor front-ends.

Then the multimeter comes out, still with the device unpowered for continuity and then briefly powered for levels:

- Find **ground** (continuity to shield, USB shell, large copper pours).
- Identify **candidate TX/RX**: a UART TX usually idles high (~3.3 V) and sits near the MCU; look for series resistors, which frequently flag debug lines.
- **Confirm logic voltage** (3.3 V vs 5 V vs 1.8 V) on every line you intend to touch, *before* you touch it with the Cardputer.

The output of this stage is a hand-drawn (or CAD) pinout map: which pad is what, at what voltage. Everything downstream references it.

### Stage 2 — UART console discovery (the highest-yield first move)

Embedded medical devices talk to themselves out loud far more often than they should, and the UART boot console is where they do it. Wire the Cardputer's UART pins to the suspected TX/RX/GND (RX-to-TX, TX-to-RX, common ground — and if in any doubt, start with RX only, so you are purely listening and cannot inject).

In BitPirate:

```
mode          # list modes, select UART
help          # UART-specific commands
# set line: 8N1 to start; BitPirate can auto-detect baud
sniff         # passive capture of whatever the device is emitting
```

Baud auto-detection saves the tedious 9600 → 115200 sweep, but I still confirm by eye: garbage that turns to clean ASCII is your baud lock. What I am reading for:

- **Bootloader banners** — U-Boot, an STM32 system bootloader, Nordic's SoftDevice init, an ESP-IDF boot log. Each names the SoC family and often the exact part and flash layout.
- **Kernel / RTOS logs** — Linux dmesg, FreeRTOS/Zephyr task output, or a bare-metal init sequence. Look for "BLE stack up", "Wi-Fi init", "sensor OK", partition tables, mount points.
- **A shell or hidden menu.** A shocking number of devices drop to a `#` prompt or a "press any key for maintenance menu" on the console. On a device you are authorised to test, that is the front door standing open.
- **Version strings and build metadata** — firmware version, build date, sometimes the toolchain, occasionally a URL or an update endpoint.

I log the whole session to the SD card (or over serial to my Mac) because the boot log is a reference document you will return to for the rest of the project.

### Stage 3 — I²C / SPI bus mapping for sensors and peripherals

This is where a medical device becomes legible as a *system*. The clinical function lives in the sensors and their front-ends, and those hang off I²C and SPI.

**I²C** — connect SDA/SCL/GND (pull-ups are usually already on the board) and:

```
mode          # select I2C
scan          # enumerate 7-bit addresses that ACK
# then, per address:
# read device/manufacturer ID registers, dump register maps
```

Every address that ACKs is a chip. Cross-reference addresses and ID registers against datasheets and you rapidly build a bill of materials of the *active* electronics: a MAX30102 for PPG/SpO₂, a pressure sensor for an occlusion line, an ADS1x9x analog front-end for ECG, a temperature sensor, an EEPROM holding calibration or a cartridge's authentication data. That last one — a small I²C EEPROM near a consumable slot — is very often where "is this cartridge genuine and not expired" is decided, and reading it non-destructively tells you a great deal about how the device thinks.

**SPI** — SCK/MOSI/MISO/CS/GND. BitPirate can act as SPI master to read SPI-NOR flash and EEPROM, and can **sniff** an active SPI bus. The external flash chip is frequently the entire firmware or filesystem image (see Stage 5). Displays, radios, and high-rate sensor front-ends also tend to live on SPI.

The deliverable from this stage is a **hardware map**: every chip, what it does, how it is addressed, its data format and update rate. That map is what turns later byte captures from noise into meaning.

### Stage 4 — Debug interfaces (JTAG/SWD), if the device permits

If Stage 1 found JTAG/SWD pads and the manufacturer has not locked them, BitPirate's JTAG scan and SWD/OpenOCD support let you:

- **Halt the CPU**, read core registers and memory.
- **Dump internal flash** — the cleanest possible firmware acquisition, when the debug port is open.

The honest caveat: **production medical devices very often fuse off or password-lock the debug port** (STM32 RDP level 1/2, nRF52 APPROTECT, ESP32 eFuse settings). If it is locked, you get little or nothing this way, and you fall back to Stage 5's other acquisition paths. Do not spend a day fighting a fused chip when the SPI flash next to it is unencrypted and unclipped.

### Stage 5 — Firmware acquisition and offline analysis

Firmware is the ground truth: it contains the protocol parsers, the state machine, the crypto (or its absence), and the update logic. Depending on what the earlier stages found, acquisition is one of:

- **JTAG/SWD dump** of internal flash (Stage 4), if unlocked.
- **UART bootloader** read-out, if the bootloader exposes a read command and it is not disabled.
- **External SPI-NOR flash read** — either in-circuit with a SOIC clip on the flash chip, or by desoldering. BitPirate reads SPI flash directly; the ADV's pin count makes the clip approach practical.

Then the analysis moves to the Mac, where BitPirate's job is done and standard reverse-engineering tools take over:

```bash
# Triidentify structure, embedded filesystems, compression, keys
binwalk -Me firmware.bin

# Entropy scan — flat high entropy suggests encryption/compression
binwalk -E firmware.bin
```

`binwalk` finds embedded SquashFS/JFFS2/LittleFS images, bootloaders, certificates, and compressed blobs. From there:

- **Ghidra / IDA** to locate the protocol handlers, the BLE GATT callbacks, the parser that turns raw bus bytes into a clinical measurement, and the update/verify routines.
- **String and symbol extraction** for endpoints, version strings, and — the finding that still turns up far too often — **hardcoded keys, credentials, or debug backdoors**.
- **Signature-check analysis**: does the update path actually verify a signature, or does it merely check a CRC? The difference is the difference between a secure device and a firmware-implant waiting to happen.

BitPirate's role here is **acquisition and live interaction**; the deep static analysis is offline, with the tools built for it.

### Stage 6 — Wireless protocol analysis

Now the radios. This is where medical devices leak, because the link is invisible and therefore easy to under-secure.

**BLE** — the most common modern medical link. BitPirate's Bluetooth mode lets you scan advertisements, connect, and enumerate services and characteristics; with a companion capable of sniffing, you can capture the connection traffic itself.

- Enumerate the **GATT table**: standard SIG health services (Heart Rate `0x180D`, Health Thermometer `0x1809`, the Continuous Glucose family, the IEEE 11073-derived services) versus **custom 128-bit UUID services** that carry the vendor's real measurement, configuration, and firmware-update traffic.
- Read/subscribe to characteristics and watch the **notifications/indications** stream as the device operates. Correlate the bytes against the sensor front-ends you identified in Stage 3 — this is where the hardware map earns its keep.
- Note the **security posture**: Just Works pairing vs passkey/OOB, whether the link is encrypted, whether the app enforces anything the device does not.

**Wi-Fi** — scan for the device's own AP or the SSIDs it seeks; observe (with authorisation, on your own isolated network) the endpoints it reaches for — a manufacturer cloud, a local gateway, a hospital integration engine.

**Sub-GHz / proprietary RF** — with a CC1101 module on the bus (or the T-Embed CC1101 as host), analyse the band, capture raw packets, and where the modulation is known, record and replay. Legacy telemetry, remote sensors, and pager-style alerting links live down here. And here the RF regulations bite as hard as the medical ones: transmitting on licensed bands, or replaying anything near a live device, is exactly what the firmware's warning and your local spectrum law forbid. Capture is one thing; transmission is a decision with legal weight.

From these captures I reconstruct message formats — headers, length fields, sequence numbers, checksums/CRCs — identify the command/response grammar, and, where it is warranted and authorised, write a small client or logger to characterise behaviour over time.

## Worked example: an infusion pump

Let me make this concrete with the device that best represents the whole problem — a **volumetric infusion pump**. I have chosen it deliberately: it is a safety-critical actuator (it moves a drug into a patient), it is a sensor system (it must detect occlusion, air-in-line, and end-of-infusion), and modern units are increasingly *connected* (dose-error-reduction libraries pushed over the network, infusion data pulled back into the EHR). It exercises every stage above. Infusion pumps are also, historically, the poster child for medical-device insecurity — the FDA's 2015 advisory on a specific pump family, and a long line of DEF CON research since, exist precisely because these constraints were once ignored.

**To be explicit about scope:** what follows is a *characterisation and defensive-review* plan on a decommissioned pump, on the bench, off the patient, off the network, with authorisation. The goal is understanding and finding weaknesses to report — not producing a technique for altering therapy on a fielded device. I will not, and you should not, cross that line.

### What a connected infusion pump looks like inside

A typical architecture:

| Subsystem | Likely implementation | BitPirate touchpoint |
|---|---|---|
| **Main controller** | STM32 / NXP Cortex-M running an RTOS; the user-facing UI and dose logic | UART console, JTAG/SWD, internal flash dump |
| **Safety controller** | A *second*, independent MCU that watches the motor and the sensors — the interlock that is supposed to stop bad therapy even if the main CPU misbehaves | Separate UART/debug pads; its own firmware |
| **Motor drive** | Stepper/peristaltic driver, position encoder | GPIO/logic capture of step/dir and encoder lines |
| **Occlusion / air-in-line sensors** | Pressure sensor + ultrasonic air detector on I²C/SPI/analog | I²C/SPI scan, register reads |
| **Dose config store** | I²C EEPROM / SPI flash holding the drug library and settings | I²C/SPI read |
| **Connectivity** | Wi-Fi and/or BLE module; sometimes a proprietary RF or a wired hospital link | Wi-Fi/BLE scan and sniff; UART to the comms module |
| **Battery / power** | Smart battery, often on SMBus (I²C) | I²C scan |

Two controllers is the detail that makes an infusion pump different from a fitness gadget. The **safety controller** is the reason the device is allowed near a patient at all, and any serious review has to ask the same question the designers did: can the main CPU, if compromised, talk the safety controller out of doing its job? That is a question you answer by reading *both* firmwares and characterising the link *between* them — not by poking the live motor.

### Targeted probing plan for the pump

Run the funnel, but pointed at this specific architecture:

**1. Recon (Stage 0).** FCC ID → radio chipset and internal photos. Service manual → connector pinouts, test-mode entry, and often the debug header location. Identify the companion drug-library software and any hospital integration (a gateway, an HL7/IHE PCD interface, or a vendor cloud).

**2. Open, map, and find the two brains (Stage 1).** Photograph the board; locate the main MCU and the *separate* safety MCU. Find debug pads for each. Identify the flash/EEPROM chips (drug library candidate), the pressure and air-in-line sensors, and the comms module. Confirm every voltage.

**3. Dual UART capture at boot (Stage 2).** Sit on the main controller's console *and*, if pins allow, the safety controller's. Capture both boot sequences. You are looking for: RTOS identity, self-test results (the pump runs a POST that exercises the sensors and the occlusion detector — the log narrates it), firmware versions of *both* MCUs, and whether either drops a maintenance/service prompt. The self-test log alone tells you how the device believes its own safety chain is wired.

**4. Sensor and drug-library bus mapping (Stage 3).** I²C `scan` to enumerate the pressure sensor, the air detector, the smart-battery (SMBus), and the config EEPROM. Read the EEPROM/flash **non-destructively**: this is where the **drug library** and **dose-error-reduction (DERR) limits** typically live. Reading it answers a genuinely important safety question — *are the hard/soft dose limits stored with any integrity protection, or is the drug library a plain, unsigned blob that anything with bus access could rewrite?* That finding is reportable and defensive; it is not, itself, an attack on a patient.

**5. Firmware of both controllers (Stages 4–5).** Try SWD on each MCU; expect at least the safety controller to be locked. Where a port is open or an external flash is readable, dump and analyse. In Ghidra, locate: the **command parser** for the comms module, the **DERR enforcement** logic (where soft/hard limits are checked against a programmed dose), the **inter-processor protocol** between main and safety MCUs, and the **update verification** path. The defensive questions are concrete — is the drug-library update signed? Is the main↔safety link authenticated or merely trusted? Does DERR fail safe?

**6. Connectivity review (Stage 6).** Enumerate the BLE GATT table or observe the Wi-Fi association and the endpoints it reaches on your isolated network. Characterise the **remote programming interface**: how a dose or a drug-library update is delivered, and — the crux — **what authenticates it**. Historically, the serious infusion-pump findings were exactly here: unauthenticated or weakly authenticated remote configuration, and drug libraries that could be altered without a signature check. You are verifying whether those classes of weakness are present, documenting them, and reporting them.

**7. Inter-processor link characterisation (defensive).** With a logic capture on the main↔safety bus (UART or SPI between the two MCUs), record the *normal* protocol during a benign, bench-only simulated infusion (saline, no patient, sensors possibly emulated). The point is to understand the safety envelope — the messages by which the safety controller confirms flow rate and asserts an interlock — so you can reason about whether that envelope holds under a misbehaving main CPU. You characterise and model the interlock; you do not attempt to defeat it on live therapy.

The whole plan converges on a small number of high-value, reportable questions: *Is the drug library integrity-protected? Is remote programming authenticated? Does the independent safety controller genuinely fail safe, and is its link to the main CPU trustworthy?* Every one of those is answered by reading and characterising — by understanding the device — which is precisely what this workstation is for.

## From the bench to Python: turning captures into evidence

This is where my usual toolchain re-enters, and where the ADV's SD card and BitPirate's Python-over-serial scripting pay off. The bench produces raw traces; Python turns them into understanding.

I export every session — UART logs, I²C/SPI dumps, BLE notification streams, logic captures — to the Mac and treat them as data, not anecdotes:

```python
import pandas as pd
import numpy as np

# BLE notifications exported as timestamped hex payloads
df = pd.read_csv("ble_notify.csv")               # ts, handle, hexpayload
df["payload"] = df.hexpayload.apply(bytes.fromhex)
df["dt_ms"]   = df.ts.diff() * 1000              # inter-notification timing

# Hypothesis: bytes 2-3 are a big-endian flow-rate field
df["field"] = df.payload.apply(lambda b: int.from_bytes(b[2:4], "big"))

# Validate against the programmed rate; check timing regularity
print(df.field.describe())
print(df.dt_ms.describe())                        # is the stream isochronous?
```

Three things I use this for repeatedly:

- **Protocol reconstruction as falsifiable hypotheses.** "Bytes 2–3 are big-endian flow rate" is a claim you can test: change the programmed rate on the bench and watch whether the field tracks. Reverse engineering done as hypothesis-and-test, logged, is the difference between a guess and a finding.
- **Sensor streams as time series.** Raw front-end data (ECG, PPG, pressure) captured at the bus is the *device's own* view, before any app-side smoothing. For any ML work on physiological signals, that distinction is not academic — a model trained on an app's post-processed output is modelling the app, not the patient. Capturing at the bus lets me verify that the data I feed a model reflects what the device actually measured.
- **Integrity and timing checks.** Is the notification stream isochronous or does it stutter? Do CRCs validate? Does the timing of the safety-controller heartbeat stay within its spec? These are quantitative, plottable, and go straight into a report.

For the clinical-AI side of my work, this closes a loop I care about a lot: the low-level understanding *validates the provenance of the data*. When I claim a model is learning from a device's measurement, I can now demonstrate — from the bus up — that it is.

## What this workstation is, and what it is not

Put together, the Cardputer/BitPirate combination lets me, in a single afternoon and from a device the size of a business card:

- **Map the hardware** — enumerate the sensors, radios, memories, and MCUs via I²C/SPI/JTAG.
- **Watch runtime behaviour** — capture boot logs, self-tests, and internal state over UART and debug.
- **Decode communication** — sniff and reconstruct BLE, Wi-Fi, and RF message formats.
- **Acquire firmware** — dump and, offline, analyse the code that implements the protocols and the safety logic.
- **Experiment safely and reproducibly** — script characterisation sequences and export everything for analysis in Python.

What it is **not** is a magic key, and it is emphatically not a licence. It will not open a properly fused debug port, defeat verified secure boot, or read an encrypted flash. It does not understand clinical protocols — it hands you the bytes and you do the semantics. And it does nothing at all that authorisation, isolation, and responsible disclosure do not first make legitimate.

That last constraint is the point, not a caveat around it. The reason I can do this work at a hospital and call it a service rather than a liability is that the discipline comes first and the cleverness second. The same instinct that made me disconnect a CT scanner from the mains before I went anywhere near its motherboard as a student is the one that keeps the pump off the patient and off the network today. The tools have become astonishingly small. The rules have not moved at all.

If you run a facility with embedded devices you cannot get answers about — a pump whose behaviour you need to validate, a monitor whose data you want to trust, a discontinued unit whose protocol died with its vendor — this is the electronic half of the repair-and-understand service I offer, and it starts exactly where the mechanical half does: with the device in front of me, and permission in writing.

---

*Sources and further reading: the [ESP32 Bit Pirate firmware repository](https://github.com/geo-tp/ESP32-Bit-Pirate) and its [project site](https://geo-tp.github.io/ESP32-Bit-Pirate/) (mode list, supported boards including the Cardputer ADV, CLI details, and the authors' usage warning); the [M5Stack Cardputer ADV](https://docs.m5stack.com/en/products) documentation for board specifications. For the medical-device security context, the FDA's [pre-market and post-market cybersecurity guidance](https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity) and CISA's [ICS medical advisories](https://www.cisa.gov/news-events/cybersecurity-advisories) are the canonical references, and the long public record of infusion-pump research presented at DEF CON and Black Hat is the reason the constraints in this post are written the way they are.*

*This post touches on medical-device security. Everything here is framed for authorised, isolated, defensive work and responsible disclosure; it is deliberately not a recipe for interfering with any device in clinical use.*
