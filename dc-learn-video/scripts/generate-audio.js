/**
 * Generate master audio track for DCLearnConvergence video.
 * All sounds are synthesized programmatically — no external files.
 *
 * Run: node scripts/generate-audio.js
 * Output: public/audio-master.wav
 */

const fs = require("fs");
const path = require("path");

const SAMPLE_RATE = 44100;
const FPS = 30;
const TOTAL_FRAMES = 1800;
const TOTAL_SECONDS = TOTAL_FRAMES / FPS; // 60
const TOTAL_SAMPLES = Math.ceil(TOTAL_SECONDS * SAMPLE_RATE);

// Master buffer — mono float samples
const master = new Float32Array(TOTAL_SAMPLES);

// Frame number → sample index
function frameToSample(frame) {
  return Math.round((frame / FPS) * SAMPLE_RATE);
}

// Add a sine tone with exponential decay
function addTone(startFrame, freq, durationMs, amplitude, decayRate) {
  const start = frameToSample(startFrame);
  const numSamples = Math.round((durationMs / 1000) * SAMPLE_RATE);
  for (let i = 0; i < numSamples; i++) {
    const t = i / SAMPLE_RATE;
    const envelope = Math.exp(-t * decayRate);
    const idx = start + i;
    if (idx >= 0 && idx < TOTAL_SAMPLES) {
      master[idx] += Math.sin(2 * Math.PI * freq * t) * amplitude * envelope;
    }
  }
}

// Add a sustained sine tone with linear fade in / fade out
function addSustained(startFrame, endFrame, freq, amplitude, fadeInFrames, fadeOutFrames) {
  const s0 = frameToSample(startFrame);
  const s1 = frameToSample(endFrame);
  const fadeInSmp = Math.round((fadeInFrames / FPS) * SAMPLE_RATE);
  const fadeOutSmp = Math.round((fadeOutFrames / FPS) * SAMPLE_RATE);
  const total = s1 - s0;
  for (let i = 0; i < total; i++) {
    const t = i / SAMPLE_RATE;
    let env = 1;
    if (i < fadeInSmp) env = i / fadeInSmp;
    if (i > total - fadeOutSmp) env = Math.min(env, (total - i) / fadeOutSmp);
    const idx = s0 + i;
    if (idx >= 0 && idx < TOTAL_SAMPLES) {
      master[idx] += Math.sin(2 * Math.PI * freq * t) * amplitude * env;
    }
  }
}

// ═══════════════════════════════════════════════════════════
// SCENE 2: CLOCK TICKS (frames 90–272)
// 8 ticks, 50ms each, 800Hz, amplitude ramps 0.3→0.5
// ═══════════════════════════════════════════════════════════
const tickFrames = [90, 116, 142, 168, 194, 220, 246, 272];
tickFrames.forEach((frame, i) => {
  const amp = 0.3 + (0.2 * i) / 7;
  // 50ms burst, decay rate 50 → reaches ~0.08 by 50ms
  addTone(frame, 800, 50, amp, 50);
});

// ═══════════════════════════════════════════════════════════
// SCENE 3: LAYERED TICKING (frames 300–360)
// 3 layers at slightly different rates, overall amp 0.25
// ═══════════════════════════════════════════════════════════
// Layer 1: 600Hz every 30 frames
for (let f = 300; f < 360; f += 30) {
  addTone(f, 600, 100, 0.25, 30);
}
// Layer 2: 700Hz every 33 frames
for (let f = 300; f < 360; f += 33) {
  addTone(f, 700, 100, 0.25, 30);
}
// Layer 3: 500Hz every 27 frames
for (let f = 300; f < 360; f += 27) {
  addTone(f, 500, 100, 0.25, 30);
}

// ═══════════════════════════════════════════════════════════
// SCENE 4: TICKING FADES OUT (360–390), CONNECTIONS (360–990)
// ═══════════════════════════════════════════════════════════

// Ticking fade-out: continue the 3 layers into 360-390 with decreasing amplitude
for (let f = 360; f < 390; f += 30) {
  addTone(f, 600, 100, 0.25 * (1 - (f - 360) / 30), 30);
}
for (let f = 363; f < 390; f += 33) {
  addTone(f, 700, 100, 0.25 * (1 - (f - 360) / 30), 30);
}
for (let f = 360; f < 390; f += 27) {
  addTone(f, 500, 100, 0.25 * (1 - (f - 360) / 30), 30);
}

// Connection tones: soft low "thum" — same base freq with slight variation
// 200ms, decay factor 3, plus 2nd harmonic for warmth
const connections = [
  { frame: 360, freq: 170 },
  { frame: 450, freq: 185 },
  { frame: 540, freq: 175 },
  { frame: 630, freq: 190 },
  { frame: 720, freq: 180 },
  { frame: 810, freq: 170 },
  { frame: 900, freq: 185 },
  { frame: 990, freq: 195 },
];
connections.forEach(({ frame, freq }) => {
  addTone(frame, freq, 200, 0.15, 3);       // fundamental
  addTone(frame, freq * 2, 200, 0.05, 3);   // 2nd harmonic for warmth
});

// ═══════════════════════════════════════════════════════════
// SCENE 4B: GREEN BUILDING CHORD (frames 1120–1330)
// C major: C3 + E3 + G3, fade in 60f, hold, fade out 60f
// Total amplitude 0.15 split across 3 notes
// ═══════════════════════════════════════════════════════════
addSustained(1120, 1330, 130, 0.05, 60, 60);  // C3
addSustained(1120, 1330, 164, 0.05, 60, 60);  // E3
addSustained(1120, 1330, 196, 0.05, 60, 60);  // G3

// ═══════════════════════════════════════════════════════════
// SCENE 5: INSIGHT (frames 1390–1560) — SILENCE
// ═══════════════════════════════════════════════════════════
// Nothing. Intentional silence. Let the text land.

// ═══════════════════════════════════════════════════════════
// SCENE 6: CLEAN TONE (frames 1560–1680)
// 261Hz middle C, fade in 30 frames to amp 0.1
// Continues into Scene 7 and fades out over 60 frames (1680–1740)
// ═══════════════════════════════════════════════════════════
addSustained(1560, 1740, 261, 0.1, 30, 60);

// ═══════════════════════════════════════════════════════════
// ENCODE WAV
// ═══════════════════════════════════════════════════════════
function encodeWAV(samples, sampleRate) {
  const numSamples = samples.length;
  const buf = Buffer.alloc(44 + numSamples * 2);

  buf.write("RIFF", 0);
  buf.writeUInt32LE(36 + numSamples * 2, 4);
  buf.write("WAVE", 8);

  buf.write("fmt ", 12);
  buf.writeUInt32LE(16, 16);       // fmt chunk size
  buf.writeUInt16LE(1, 20);        // PCM
  buf.writeUInt16LE(1, 22);        // mono
  buf.writeUInt32LE(sampleRate, 24);
  buf.writeUInt32LE(sampleRate * 2, 28); // byte rate
  buf.writeUInt16LE(2, 32);        // block align
  buf.writeUInt16LE(16, 34);       // bits per sample

  buf.write("data", 36);
  buf.writeUInt32LE(numSamples * 2, 40);

  for (let i = 0; i < numSamples; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    const val = s < 0 ? s * 0x8000 : s * 0x7FFF;
    buf.writeInt16LE(Math.round(val), 44 + i * 2);
  }

  return buf;
}

const wav = encodeWAV(master, SAMPLE_RATE);
const outPath = path.join(__dirname, "..", "public", "audio-master.wav");
fs.writeFileSync(outPath, wav);

const sizeMB = (wav.length / (1024 * 1024)).toFixed(2);
console.log(`Written: ${outPath} (${sizeMB} MB, ${TOTAL_SECONDS}s, ${SAMPLE_RATE}Hz mono)`);
