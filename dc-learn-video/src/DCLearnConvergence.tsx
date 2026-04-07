import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Img,
  staticFile,
  interpolateColors,
} from "remotion";

// ── Data ──────────────────────────────────────────────
const CLOCKS = [
  { name: "EU Taxonomy", stat: "PUE ≤1.3", color: "#D4A84B", angle: 270, behavior: "steady" },
  { name: "F-Gas Phase-Down", stat: "R-410A · GWP 2,088", color: "#E06060", angle: 315, behavior: "counter" },
  { name: "CRU 80% Renewable", stat: "Currently at 40%", color: "#4a7c59", angle: 0, behavior: "stuck" },
  { name: "EED Article 12", stat: "Annual reporting due", color: "#5B9BD5", angle: 45, behavior: "fast" },
  { name: "Carbon Tax", stat: "€71 → €100/tCO₂", color: "#fb923c", angle: 90, behavior: "accelerating" },
  { name: "Grid Constraints", stat: "5 MVA since 2013", color: "#a78bfa", angle: 135, behavior: "frozen" },
  { name: "CRREM Misalignment", stat: "Profitable & misaligned", color: "#e879a0", angle: 180, behavior: "redRing" },
  { name: "Fire Suppression", stat: "FM-200 · GWP 3,220", color: "#C75050", angle: 225, behavior: "pulse" },
];

const CONNECTIONS = [
  { from: 1, to: 7, label: "Same regulation. Different systems.", primary: true, start: 360 },
  { from: 0, to: 3, label: "Can’t report what you can’t measure.", primary: true, start: 465 },
  { from: 0, to: 5, label: "Lower the PUE. Free the headroom. Enable the density.", primary: true, start: 570 },
  { from: 2, to: 4, label: "The PPA that fixes one reduces the other.", primary: true, start: 675 },
  { from: 0, to: 6, label: "PUE drives the carbon that drives misalignment.", primary: false, start: 750 },
  { from: 1, to: 0, label: "Replace the condenser. Fix the cooling. Same job.", primary: false, start: 810 },
  { from: 3, to: 2, label: "The metering that proves EED compliance is the same metering CRU needs.", primary: false, start: 855 },
  { from: 5, to: 4, label: "When the grid can’t give you more, you generate your own.", primary: false, start: 900 },
];

const LARGE_TERMS = [
  { text: "PUE", color: "#D4A84B", angle: 270 },
  { text: "F-Gas", color: "#E06060", angle: 315 },
  { text: "CRU", color: "#4a7c59", angle: 0 },
  { text: "EED", color: "#5B9BD5", angle: 45 },
  { text: "Carbon Tax", color: "#fb923c", angle: 90 },
  { text: "Grid", color: "#a78bfa", angle: 135 },
  { text: "CRREM", color: "#e879a0", angle: 180 },
  { text: "Fire", color: "#C75050", angle: 225 },
];

const MEDIUM_TERMS = [
  "containment", "free cooling", "delta-T", "MIC", "VESDA", "Novec 1230", "HVO", "CDU",
  "concurrent maintainability", "BESS", "N+1", "ATS", "redundancy", "topology", "DCIM", "BMS",
];

const SMALL_TERMS = [
  "thermal runaway", "PDU whip", "48-hour fuel", "Icw rating", "discrimination study",
  "Scope 2 market-based", "additionality", "€/kW", "elemental cost plan", "lifecycle cost",
  "WAULT", "cap rate", "IS 10101", "EN 50600", "EN 61439", "CIBSE TM40", "GHG Protocol",
  "NEAP", "SLA", "dry coolers", "chillers",
];

// ── Helpers ───────────────────────────────────────────
const fadeIn = (f: number, start: number, dur = 15) =>
  interpolate(f, [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

const clockPos = (
  angle: number,
  cx: number,
  cy: number,
  rx: number,
  ry: number
) => {
  const rad = (angle * Math.PI) / 180;
  return { x: cx + rx * Math.cos(rad), y: cy + ry * Math.sin(rad) };
};

const getHandAngle = (behavior: string, frame: number): number => {
  switch (behavior) {
    case "steady": return frame * 2;
    case "counter": return frame * -2;
    case "stuck": return 144;
    case "fast": return frame * 4;
    case "accelerating": return frame * frame * 0.001;
    case "frozen": return 0;
    case "redRing": return frame * 2;
    case "pulse": return frame * 2;
    default: return frame * 2;
  }
};

// ── Component ─────────────────────────────────────────
export const DCLearnConvergence: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const cx = 960;
  const cy = 520;
  const ringRadius = 420;

  // Building color transition (870-930)
  const greenT = interpolate(frame, [870, 930], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const rackStroke = interpolateColors(greenT, [0, 1], ["#3d444d", "#4a7c59"]);
  const rackFill = interpolateColors(greenT, [0, 1], ["#1c2128", "rgba(74,124,89,0.15)"]);
  const outlineStroke = interpolateColors(greenT, [0, 1], ["#3d444d", "#4a7c59"]);

  // Scene visibility
  const openingOpacity = fadeIn(frame, 15, 30);
  const clocksVisible = frame >= 90;
  const insightOverlay = frame >= 930 && frame < 1140 ? fadeIn(frame, 930, 20) : 0;
  const clockDim = frame >= 930 ? 0.15 : 1;
  const scene6 = frame >= 1140 && frame < 1380;
  const scene7 = frame >= 1380;

  // Connection label: which is active
  const activeConn = CONNECTIONS.reduce<number | null>((acc, c, i) => {
    const dur = c.primary ? 105 : 75;
    if (frame >= c.start && frame < c.start + dur) return i;
    return acc;
  }, null);

  // Clock positions array for connections
  const clockPositions = CLOCKS.map((c) => clockPos(c.angle, cx, cy, ringRadius, ringRadius));

  // Bezier that avoids building centre, starts/ends at clock perimeter
  const connPath = (fromIdx: number, toIdx: number) => {
    const p1 = clockPositions[fromIdx];
    const p2 = clockPositions[toIdx];

    // FIX 6: offset start/end to clock perimeter (36px radius)
    const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);
    const perimR = 36;
    const sx = p1.x + Math.cos(angle) * perimR;
    const sy = p1.y + Math.sin(angle) * perimR;
    const ex = p2.x - Math.cos(angle) * perimR;
    const ey = p2.y - Math.sin(angle) * perimR;

    // FIX 7: control point perpendicular to line, pushed AWAY from building centre
    const mx = (sx + ex) / 2;
    const my = (sy + ey) / 2;
    const perpX = -(p2.y - p1.y);
    const perpY = p2.x - p1.x;
    const perpLen = Math.sqrt(perpX * perpX + perpY * perpY) || 1;
    const npx = perpX / perpLen;
    const npy = perpY / perpLen;
    // pick the perpendicular direction that moves AWAY from (cx, cy)
    const d1 = (mx + npx * 150 - cx) ** 2 + (my + npy * 150 - cy) ** 2;
    const d2 = (mx - npx * 150 - cx) ** 2 + (my - npy * 150 - cy) ** 2;
    const sign = d1 >= d2 ? 1 : -1;
    const cpx = mx + npx * 150 * sign;
    const cpy = my + npy * 150 * sign;

    return "M " + sx + " " + sy + " Q " + cpx + " " + cpy + " " + ex + " " + ey;
  };

  // ── SCENE 6: COURSE REVEAL ──
  if (scene6) {
    return (
      <AbsoluteFill style={{ backgroundColor: "#0a0e14" }}>
        {/* DC-LEARN label */}
        <div style={{
          position: "absolute", left: "50%", top: 340, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1140),
          fontFamily: "monospace", color: "#4a7c59", fontSize: 14,
          textTransform: "uppercase", letterSpacing: 4,
        }}>
          DC-LEARN
        </div>

        {/* Headline */}
        <div style={{
          position: "absolute", left: "50%", top: 410, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1160, 18),
          fontFamily: "Georgia, serif", fontSize: 46, color: "white",
          textAlign: "center", maxWidth: 900, lineHeight: 1.2,
        }}>
          The only learning resource that shows how they connect.
        </div>

        {/* Three stat columns */}
        <div style={{
          position: "absolute", left: "50%", top: 500, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1230),
          display: "flex", alignItems: "flex-start", gap: 0,
        }}>
          {([
            { num: "15", label: "CHAPTERS", sub: "The Data Centre Clock" },
            { num: "16", label: "MODULES", sub: null },
            { num: "5", label: "PERSONAS", sub: null },
          ] as const).map((col, i) => (
            <React.Fragment key={col.label}>
              {i > 0 && (
                <div style={{ width: 1, height: 70, backgroundColor: "#1c2128", margin: "0 40px" }} />
              )}
              <div style={{ textAlign: "center", minWidth: 80 }}>
                <div style={{ fontFamily: "Georgia, serif", fontSize: 52, color: "white" }}>{col.num}</div>
                <div style={{ fontFamily: "monospace", fontSize: 11, color: "#57606a", letterSpacing: 2 }}>{col.label}</div>
                {col.sub && (
                  <div style={{ fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 13, color: "#8b949e", marginTop: 6 }}>
                    {col.sub}
                  </div>
                )}
              </div>
            </React.Fragment>
          ))}
        </div>

        {/* Bottom lines */}
        <div style={{
          position: "absolute", left: "50%", top: 600, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1290),
          fontFamily: "monospace", fontSize: 15, color: "#8b949e", textAlign: "center",
        }}>
          Story teaches the why. Modules teach the how.
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 625, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1335),
          fontFamily: "monospace", fontSize: 15, color: "#8b949e", textAlign: "center",
        }}>
          Irish standards. Irish grid. Irish deadlines.
        </div>
      </AbsoluteFill>
    );
  }

  // ── SCENE 7: END SCREEN — holds until end ──
  if (scene7) {
    const logoCY = 360; // logo centre y for word cloud ring
    const cloudR = 300; // large term ring radius
    return (
      <AbsoluteFill style={{ backgroundColor: "#0a0e14" }}>
        {/* "Three chapters. Three modules." */}
        <div style={{
          position: "absolute", left: "50%", top: 200, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1380),
          fontFamily: "Georgia, serif", fontSize: 48, color: "white", textAlign: "center",
        }}>
          Three chapters. Three modules.
        </div>

        {/* "Free." */}
        <div style={{
          position: "absolute", left: "50%", top: 280, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1440),
          fontFamily: "Georgia, serif", fontSize: 68, color: "#4a7c59",
        }}>
          Free.
        </div>

        {/* Logo — 100px circular clip */}
        <div style={{
          position: "absolute", left: "50%", top: logoCY, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1500),
          width: 100, height: 100, borderRadius: "50%", overflow: "hidden",
          border: "2px solid #4a7c59",
          display: "flex", alignItems: "center", justifyContent: "center",
          background: "#0a0e14",
        }}>
          <Img src={staticFile("logo_only.png")} style={{ width: 120, height: 120, objectFit: "cover" }} />
        </div>

        {/* DC-LEARN */}
        <div style={{
          position: "absolute", left: "50%", top: 470, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1530),
          fontFamily: "Georgia, serif", fontWeight: "bold", fontSize: 42, color: "#4a7c59",
        }}>
          DC-LEARN
        </div>

        {/* Tagline */}
        <div style={{
          position: "absolute", left: "50%", top: 505, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1545),
          fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 16, color: "#8b949e",
        }}>
          The convergence course for data centre professionals
        </div>

        {/* Word cloud — rings centred on logo, constrained to y=180-950 */}
        <div style={{ opacity: fadeIn(frame, 1560), position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}>
          {/* Large coloured terms at radius 300 */}
          {LARGE_TERMS.map((t) => {
            const pos = clockPos(t.angle, cx, logoCY, cloudR, cloudR);
            // Clamp to word cloud zone (y 180-950)
            const clampedY = Math.max(180, Math.min(950, pos.y));
            return (
              <span key={t.text} style={{
                position: "absolute", left: pos.x, top: clampedY,
                transform: "translate(-50%,-50%)",
                fontFamily: "monospace", fontSize: 16, color: t.color, opacity: 0.7,
              }}>
                {t.text}
              </span>
            );
          })}
          {/* Medium white terms */}
          {MEDIUM_TERMS.map((t, i) => {
            const a = (i / MEDIUM_TERMS.length) * 360 + 11;
            const pos = clockPos(a, cx, logoCY, cloudR + 80, cloudR + 80);
            const clampedY = Math.max(180, Math.min(950, pos.y));
            return (
              <span key={t} style={{
                position: "absolute", left: pos.x, top: clampedY,
                transform: "translate(-50%,-50%)",
                fontFamily: "monospace", fontSize: 12, color: "white", opacity: 0.5,
              }}>
                {t}
              </span>
            );
          })}
          {/* Small dim terms */}
          {SMALL_TERMS.map((t, i) => {
            const a = (i / SMALL_TERMS.length) * 360 + 7;
            const pos = clockPos(a, cx, logoCY, cloudR + 200, cloudR + 200);
            const clampedY = Math.max(180, Math.min(950, pos.y));
            return (
              <span key={t} style={{
                position: "absolute", left: pos.x, top: clampedY,
                transform: "translate(-50%,-50%)",
                fontFamily: "monospace", fontSize: 10, color: "white", opacity: 0.28,
              }}>
                {t}
              </span>
            );
          })}
        </div>

        {/* legacybe.ie */}
        <div style={{
          position: "absolute", left: "50%", top: 980, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1590),
          fontFamily: "monospace", fontSize: 12, color: "#4a7c59",
        }}>
          legacybe.ie
        </div>
      </AbsoluteFill>
    );
  }

  // ── SCENES 1–5 ──
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e14" }}>
      {/* Scene 1: Opening */}
      <div style={{ opacity: openingOpacity, position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}>
        {/* Logo at y=390 (centred) */}
        <div style={{
          position: "absolute", left: "50%", top: 390, transform: "translate(-50%, -50%)",
          width: 80, height: 80, borderRadius: "50%", overflow: "hidden",
          border: "2px solid #4a7c59",
          display: "flex", alignItems: "center", justifyContent: "center",
          background: "#0a0e14",
        }}>
          <Img src={staticFile("logo_only.png")} style={{ width: 100, height: 100, objectFit: "cover" }} />
        </div>

        {/* Building racks at y=460 */}
        <svg width={160} height={70} viewBox="0 0 160 70" style={{ position: "absolute", left: cx - 80, top: 460 }}>
          <rect x={10} y={10} width={140} height={50} fill="none" stroke={outlineStroke} strokeWidth={2} rx={4} />
          {[0, 1, 2, 3, 4].map((i) => {
            const rw = 20;
            const rh = 36;
            const gap = (140 - 5 * rw) / 6;
            const rx2 = 10 + gap + i * (rw + gap);
            const ry2 = 10 + (50 - rh) / 2;
            return (
              <React.Fragment key={i}>
                <rect x={rx2} y={ry2} width={rw} height={rh} fill={rackFill} stroke={rackStroke} strokeWidth={1.5} rx={2} />
                {greenT > 0.5 && (
                  <circle cx={rx2 + rw / 2} cy={ry2 + 6} r={3} fill="#4a7c59" opacity={greenT} />
                )}
              </React.Fragment>
            );
          })}
          <line x1={10} y1={60} x2={150} y2={60} stroke={outlineStroke} strokeWidth={2} />
          {greenT > 0 && (
            <rect x={6} y={6} width={148} height={58} fill="none" stroke="#4a7c59" strokeWidth={4} rx={6} opacity={0.15 * greenT} />
          )}
        </svg>

        {/* "CLONSHAUGH DATA CENTRE" at y=530 */}
        <div style={{ position: "absolute", left: "50%", top: 530, transform: "translateX(-50%)", fontFamily: "monospace", color: "#4a7c59", fontSize: 14, letterSpacing: 6, textTransform: "uppercase", whiteSpace: "nowrap" }}>
          Clonshaugh Data Centre
        </div>

        {/* Stats at y=555 */}
        <div style={{ position: "absolute", left: "50%", top: 555, transform: "translateX(-50%)", fontFamily: "monospace", color: "#57606a", fontSize: 13, whiteSpace: "nowrap" }}>
          400 racks · 2.4 MW · PUE 1.50 · Built 2013
        </div>

        {/* Dublin at y=580 */}
        <div style={{ position: "absolute", left: "50%", top: 580, transform: "translateX(-50%)", fontFamily: "monospace", color: "#3d444d", fontSize: 12 }}>
          Dublin
        </div>

        {/* Building green text (4B) — appears at frame 900 */}
        {frame >= 900 && (
          <>
            <div style={{ position: "absolute", left: "50%", top: 610, transform: "translateX(-50%)", opacity: fadeIn(frame, 900), fontFamily: "monospace", color: "#4a7c59", fontSize: 16, fontWeight: "bold", whiteSpace: "nowrap" }}>
              Understood. Aligned. Ahead of the clock.
            </div>
            <div style={{ position: "absolute", left: "50%", top: 632, transform: "translateX(-50%)", opacity: fadeIn(frame, 900), fontFamily: "monospace", color: "#57606a", fontSize: 12, whiteSpace: "nowrap" }}>
              The building that understands what’s coming.
            </div>
          </>
        )}
      </div>

      {/* Clocks layer */}
      {clocksVisible && (
        <svg style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", opacity: clockDim }}>
          {CLOCKS.map((clock, i) => {
            const appearFrame = 90 + i * 26;
            const opacity = fadeIn(frame, appearFrame, 12);
            if (opacity <= 0) return null;
            const pos = clockPositions[i];
            const handAngle = getHandAngle(clock.behavior, frame - appearFrame);
            const r = 32;
            const handLen = 22;
            const hx = handLen * Math.cos(((handAngle - 90) * Math.PI) / 180);
            const hy = handLen * Math.sin(((handAngle - 90) * Math.PI) / 180);

            // Text scale animation
            const textScale = interpolate(frame, [appearFrame, appearFrame + 15], [2, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });

            // Ring color for CRREM
            const ringColor = clock.behavior === "redRing" && frame > 600 ? "#E06060" : clock.color;

            // Pulse for Fire Suppression
            const pulseOp = clock.behavior === "pulse" ? 0.5 + 0.5 * Math.sin(frame * 0.15) : 1;

            // Label position
            const isTop = clock.angle >= 225 || clock.angle <= 315 && clock.angle >= 225;
            const isBottom = clock.angle >= 45 && clock.angle <= 135;
            const isLeft = clock.angle === 180;
            const isRight = clock.angle === 0;

            let labelX = pos.x;
            let labelY = pos.y + r + 18;
            let textAnchor: "start" | "middle" | "end" = "middle";
            if (isBottom) { labelY = pos.y - r - 30; }
            if (isLeft) { labelX = pos.x + r + 10; labelY = pos.y; textAnchor = "start"; }
            if (isRight) { labelX = pos.x - r - 10; labelY = pos.y; textAnchor = "end"; }

            return (
              <g key={i} opacity={opacity}>
                <circle cx={pos.x} cy={pos.y} r={r} fill="rgba(10,14,20,0.7)" stroke={ringColor} strokeWidth={2.5} />
                <line x1={pos.x} y1={pos.y} x2={pos.x + hx} y2={pos.y + hy} stroke={clock.color} strokeWidth={2} strokeLinecap="round" />
                <circle cx={pos.x} cy={pos.y} r={3} fill={clock.color} />
                <g style={{ transformOrigin: labelX + "px " + labelY + "px", transform: "scale(" + textScale + ")" }}>
                  <text x={labelX} y={labelY} textAnchor={textAnchor} fill={clock.color} fontFamily="monospace" fontSize={16} fontWeight="bold">
                    {clock.name}
                  </text>
                  <text x={labelX} y={labelY + 16} textAnchor={textAnchor} fill={clock.color} fontFamily="monospace" fontSize={13} opacity={clock.behavior === "pulse" ? pulseOp : 0.8}>
                    {clock.stat}
                  </text>
                </g>
              </g>
            );
          })}
        </svg>
      )}

      {/* Connections SVG — dashed, animated, perimeter-to-perimeter */}
      {frame >= 360 && frame < 930 && (
        <svg style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}>
          {CONNECTIONS.map((conn, i) => {
            if (frame < conn.start) return null;
            const isActive = activeConn === i;
            const lineOpacity = isActive ? 0.7 : 0.2;
            const path = connPath(conn.from, conn.to);
            return (
              <path
                key={i}
                d={path}
                fill="none"
                stroke="#c9d1d9"
                strokeWidth={isActive ? 2.5 : 1}
                opacity={lineOpacity}
                strokeDasharray="8 6"
                strokeDashoffset={-(frame * 1.2)}
              />
            );
          })}
        </svg>
      )}

      {/* Connection label — pill at y=980, one at a time */}
      {activeConn !== null && frame < 930 && (
        <div style={{
          position: "absolute", left: "50%", top: 980, transform: "translate(-50%, -50%)",
          backgroundColor: "#0a0e14",
          border: "1px solid " + CLOCKS[CONNECTIONS[activeConn].from].color + "4d",
          padding: "10px 24px", borderRadius: 8,
        }}>
          <div style={{
            fontFamily: "monospace", fontStyle: "italic",
            fontSize: CONNECTIONS[activeConn].primary ? 18 : 15,
            color: "#c9d1d9", textAlign: "center", whiteSpace: "nowrap",
          }}>
            {CONNECTIONS[activeConn].label}
          </div>
        </div>
      )}

      {/* Scene 3 overlay text */}
      {frame >= 300 && frame < 360 && (
        <div style={{ position: "absolute", bottom: 80, left: "50%", transform: "translateX(-50%)", opacity: fadeIn(frame, 300) }}>
          <div style={{ fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 36, color: "rgba(255,255,255,0.7)", textAlign: "center", whiteSpace: "nowrap" }}>
            Eight regulations. One building. All ticking.
          </div>
        </div>
      )}

      {/* Scene 5: Insight overlay — absolute positioned, translateY entrance */}
      {insightOverlay > 0 && (
        <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(10,14,20," + (0.88 * insightOverlay) + ")" }}>
          {[
            { text: "They weren’t designed by the same people.", start: 945, y: 400, size: 44, color: "white", font: "Georgia, serif", style: "italic" as const },
            { text: "They weren’t drafted in the same year.", start: 1020, y: 460, size: 44, color: "white", font: "Georgia, serif", style: "italic" as const },
            { text: "But they all land on the same building, in the same decade.", start: 1080, y: 530, size: 48, color: "#4a7c59", font: "Georgia, serif", style: "italic" as const },
          ].map((line) => {
            const op = fadeIn(frame, line.start);
            const ty = interpolate(frame, [line.start, line.start + 15], [12, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            return (
              <div key={line.start} style={{
                position: "absolute", left: "50%", top: line.y,
                transform: "translate(-50%, " + ty + "px)",
                opacity: op, fontFamily: line.font, fontStyle: line.style,
                fontSize: line.size, color: line.color,
                textAlign: "center", maxWidth: "80%", whiteSpace: "nowrap",
              }}>
                {line.text}
              </div>
            );
          })}
          {(() => {
            const op4 = fadeIn(frame, 1110);
            const ty4 = interpolate(frame, [1110, 1125], [12, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            return (
              <div style={{
                position: "absolute", left: "50%", top: 590,
                transform: "translate(-50%, " + ty4 + "px)",
                opacity: op4, fontFamily: "monospace", fontSize: 14, color: "#57606a",
                textTransform: "uppercase", letterSpacing: 2,
                textAlign: "center", maxWidth: "80%", whiteSpace: "nowrap",
              }}>
                Nobody coordinated them. But the deadlines coordinated themselves.
              </div>
            );
          })()}
        </div>
      )}
    </AbsoluteFill>
  );
};
