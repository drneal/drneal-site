---
title: "Binaural Beat Generator: Web Audio API, Psychoacoustics, and Client-Side WAV Export"
date: 2026-06-20
category: Engineering
tags: Web Audio API, JavaScript, DSP, psychoacoustics, binaural beats, OfflineAudioContext, WAV, neuroscience, sound design
level: Intermediate
read_time: 8 min
summary: How the Binaural Beat Generator works — Web Audio API graph construction, real-time oscilloscope rendering, brainwave frequency bands, and exporting a 60-second stereo WAV entirely client-side using OfflineAudioContext.
featured: false
---

*The tool is live at [/binaural](/binaural). Use headphones — the binaural effect does not work on speakers. Pick a preset, hit play, and the oscilloscope shows the summed waveform in real time.*

---

Binaural beats are one of those rare phenomena where the neuroscience, the psychoacoustics, and the engineering are all independently interesting. This post covers all three, and explains why the entire thing — including WAV export of a 60-second stereo file — runs entirely in the browser without touching a server.

## The Physics: Why Two Tones Make a Third

When you play a pure 200 Hz sine wave in your left ear and a 210 Hz sine wave in your right ear, you hear a tone that pulses at 10 Hz. This is the binaural beat — a tone at the *difference* frequency, perceived as a rhythmic amplitude modulation even though neither ear receives it directly.

The mechanism is neural rather than acoustic. In monaural beating (two tones in the same ear), the interference is physical — the soundwaves superpose in the air column of your ear canal to produce a real 10 Hz amplitude envelope. With binaural beats, the two tones are acoustically isolated, delivered to separate ears through headphones. The "beat" is constructed entirely by the superior olivary complex in the brainstem, the same structure responsible for sound localisation via interaural time differences. The brain's attempt to reconcile two slightly different frequencies across ears generates a coherent oscillation at the difference frequency.

This is why the effect requires headphones. On speakers, the acoustic signals mix in the room before reaching your ears, producing conventional monaural beating rather than a binaural neural phenomenon.

## The Web Audio API Graph

The generator is built entirely on the [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API), a graph-based audio processing system available in all modern browsers. The signal graph for the binaural beat is minimal:

```
OscillatorNode (L: carrier Hz)   ──→ ChannelMergerNode (input 0 → left channel)  ──→ GainNode ──→ AnalyserNode ──→ AudioContext.destination
OscillatorNode (R: carrier+Δ Hz) ──→ ChannelMergerNode (input 1 → right channel) ──→ (same)
```

The `ChannelMergerNode` is the key component — it takes two mono inputs and maps them to the left and right channels of a stereo output. Without the merger, both oscillators would appear in both ears and you'd get monaural beating in each ear rather than a binaural beat across them.

```javascript
const audioCtx = new AudioContext();
const merger   = audioCtx.createChannelMerger(2);
const gain     = audioCtx.createGain();
const analyser = audioCtx.createAnalyser();

const oscL = audioCtx.createOscillator();
const oscR = audioCtx.createOscillator();
oscL.frequency.setValueAtTime(carrier,          audioCtx.currentTime);
oscR.frequency.setValueAtTime(carrier + beatHz, audioCtx.currentTime);

oscL.connect(merger, 0, 0);   // input 0 → left channel
oscR.connect(merger, 0, 1);   // input 0 → right channel
merger.connect(gain);
gain.connect(analyser);
analyser.connect(audioCtx.destination);

oscL.start();
oscR.start();
```

Parameter changes during playback use `setTargetAtTime()` rather than `setValueAtTime()` to avoid clicks — the exponential ramp smooths the frequency transition over a 50ms time constant.

## Waveforms

All four waveform types available in `OscillatorNode` are exposed:

**Sine** is the purest binaural source and the one used in almost all psychoacoustics research. The absence of harmonics means the beat frequency is uncontaminated by harmonic interactions between the two signals.

**Triangle** adds odd harmonics at 3rd, 5th, 7th... with amplitudes falling off at 1/n². The harmonics generate secondary binaural beats at multiples of the fundamental beat frequency (3Δ, 5Δ, 7Δ), producing a richer perceived texture.

**Square** contains the same odd harmonics as triangle but with amplitudes falling at only 1/n — much stronger upper harmonics, giving a buzzier character. The secondary beats are correspondingly louder.

**Sawtooth** contains all harmonics (both odd and even) at 1/n amplitude — the brightest waveform, generating a dense harmonic stack of secondary binaural beats across the audible spectrum.

For most use cases (meditation, focus, sleep), sine is the right choice. The other waveforms are more interesting from a DSP and synthesis perspective than a neuroscientific one.

## Brainwave Frequency Bands

The preset buttons map to the five canonical EEG frequency bands. These are the bands you'd record from scalp electrodes, and the claim behind binaural beat entrainment is that sustained exposure to a binaural beat at a given frequency encourages the brain to increase power in the corresponding EEG band — a phenomenon called *frequency-following response*.

The research on entrainment is genuinely mixed. There's reasonable evidence for modest effects on subjective states and some EEG measures, particularly in the theta and alpha bands. The gamma literature is thinner and the effect sizes across all bands are small. I've included the presets because they're the conventional framing for the tool and are useful as starting points — not because I'm claiming clinical efficacy.

**Delta (0.5–4 Hz):** The dominant frequency during deep dreamless sleep and in deeply anaesthetised states. Default preset: 100 Hz carrier, 2 Hz beat.

**Theta (4–8 Hz):** Associated with drowsiness, light sleep, and certain meditative states. Also the frequency range observed during REM sleep and during focused attention to internal imagery. Default preset: 150 Hz carrier, 6 Hz beat.

**Alpha (8–13 Hz):** The "idle rhythm" — prominent when eyes are closed and the mind is relaxed but not asleep. Reduced during active visual processing (Berger's alpha attenuation). Default preset: 200 Hz carrier, 10 Hz beat.

**Beta (13–30 Hz):** The dominant awake rhythm during active cognitive engagement — problem solving, active conversation, decision making. Higher beta frequencies are sometimes associated with anxiety. Default preset: 220 Hz carrier, 18 Hz beat.

**Gamma (30–100 Hz):** Associated with high-level cognitive binding, perceptual grouping, and working memory maintenance. The 40 Hz gamma oscillation is particularly studied in the context of consciousness research. Default preset: 300 Hz carrier, 40 Hz beat.

**Schumann resonance (7.83 Hz):** The fundamental electromagnetic resonance frequency of the Earth-ionosphere cavity, driven primarily by global lightning discharge. It sits in the theta/alpha border. Its inclusion here is more aesthetically motivated than neuroscientific.

## The Oscilloscope Visualiser

The `AnalyserNode` in the signal graph provides time-domain waveform data via `getByteTimeDomainData()`, which returns 2048 samples of the summed mono output as unsigned 8-bit integers centred at 128.

The canvas renderer runs in a `requestAnimationFrame` loop, mapping each sample to a y-coordinate:

```javascript
const buf = new Uint8Array(analyser.frequencyBinCount);
analyser.getByteTimeDomainData(buf);
const slice = width / buf.length;
ctx.beginPath();
for (let i = 0; i < buf.length; i++) {
  const y = ((buf[i] / 128) - 1) * (height / 2) + height / 2;
  if (i === 0) ctx.moveTo(0, y);
  else ctx.lineTo(i * slice, y);
}
ctx.stroke();
```

Note that the visualiser sees the *merged stereo signal* from the analyser — which sits downstream of the channel merger — but the `AnalyserNode` operates on whatever signal it receives without distinguishing channels. In practice it shows the left-channel waveform (first channel of the merger output), since the default behaviour of an AnalyserNode connected to stereo audio is to analyse the first (left) channel. This is fine for visualisation purposes — the right channel is an identical waveform at a slightly different frequency, indistinguishable by eye at the frequency resolution we're working with.

## WAV Export via OfflineAudioContext

This is the most technically interesting part of the implementation. The `OfflineAudioContext` renders audio faster than real-time into a buffer without sending anything to hardware speakers. It takes the same graph as the live playback context but renders to a `AudioBuffer` directly.

```javascript
const duration   = 60;
const sampleRate = 44100;
const offCtx = new OfflineAudioContext(2, sampleRate * duration, sampleRate);

// Same graph as live playback, connected to offCtx.destination
offL.connect(offMerger, 0, 0);
offR.connect(offMerger, 0, 1);
offMerger.connect(offGain);
offGain.connect(offCtx.destination);

offL.start(0);
offR.start(0);

const rendered = await offCtx.startRendering();  // returns AudioBuffer
```

The rendered `AudioBuffer` contains two channels of 32-bit float samples. Converting this to a WAV file requires writing a standard RIFF/WAV header (44 bytes) followed by interleaved 16-bit signed PCM samples — a simple binary encoding step that runs synchronously in JavaScript.

The interleaving loop:
```javascript
for (let i = 0; i < numSamples; i++) {
  for (let c = 0; c < numChannels; c++) {
    const s = Math.max(-1, Math.min(1, channels[c][i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    offset += 2;
  }
}
```

The resulting 60-second 44.1 kHz stereo WAV is approximately 10 MB. The entire process — rendering and encoding — completes in under 2 seconds on a modern machine, all in the browser without any server round-trip.

The exported filename encodes the settings: `binaural_200hz_10p0hz_sine.wav`, making it easy to distinguish files if you're doing a systematic exploration of different configurations.

## On the Evidence for Brainwave Entrainment

This is a tool built by someone who studied medicine and has spent years with modular synthesisers and audio DSP. I find the psychoacoustics genuinely interesting and the signal processing elegant. The neuroscience is considerably murkier.

The frequency-following response — where sustained binaural exposure at frequency f increases EEG power at f — has been observed in multiple studies, though effect sizes are modest and there's substantial inter-individual variation. The leap from "EEG shows more alpha power" to "subjectively more relaxed" is plausible but not robustly demonstrated in controlled trials. The commercial wellness claims for binaural beats are well ahead of the evidence.

What the tool is good for: a clean, configurable binaural tone source for personal experimentation, meditation soundscaping, or DSP prototyping. Use sine at alpha or theta frequencies with headphones, give it 10–15 minutes, and form your own impression. The WAV export means you can integrate it into a DAW session or a longer recorded practice.

---

*[Open the Binaural Beat Generator](/binaural) — headphones required. The oscilloscope shows the carrier waveform; the beat is perceived, not visible at this time resolution.*
