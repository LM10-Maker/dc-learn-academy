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
  const rackFill = interpolateColors(greenT, [0, 1], ["#1c2128", "#1a3d24"]);
  const outlineStroke = interpolateColors(greenT, [0, 1], ["#3d444d", "#4a7c59"]);

  // Scene visibility
  const openingOpacity = fadeIn(frame, 15, 30);
  const clocksVisible = frame >= 90;
  const insightOverlay = frame >= 930 && frame < 1140 ? fadeIn(frame, 930, 15) : 0;
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

  // Bezier that avoids center
  const connPath = (fromIdx: number, toIdx: number) => {
    const p1 = clockPositions[fromIdx];
    const p2 = clockPositions[toIdx];
    const mx = (p1.x + p2.x) / 2;
    const my = (p1.y + p2.y) / 2;
    const dx = mx - cx;
    const dy = my - cy;
    const dist = Math.sqrt(dx * dx + dy * dy) || 1;
    const offset = 120;
    const cpx = mx + (dx / dist) * offset;
    const cpy = my + (dy / dist) * offset;
    return "M " + p1.x + " " + p1.y + " Q " + cpx + " " + cpy + " " + p2.x + " " + p2.y;
  };

  // ── SCENE 6: COURSE REVEAL ──
  if (scene6) {
    return (
      <AbsoluteFill style={{ backgroundColor: "#0a0e14" }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", gap: 16 }}>
          <div style={{ opacity: fadeIn(frame, 1140), fontFamily: "monospace", color: "#4a7c59", fontSize: 14, textTransform: "uppercase", letterSpacing: 8 }}>
            DC-LEARN
          </div>
          <div style={{ opacity: fadeIn(frame, 1158), fontFamily: "Georgia, serif", color: "white", fontSize: 46, textAlign: "center", maxWidth: "80%", lineHeight: 1.2, marginTop: 16 }}>
            The only learning resource that shows how they connect.
          </div>
          <div style={{ opacity: fadeIn(frame, 1230), display: "flex", gap: 80, marginTop: 40 }}>
            {[["15", "CHAPTERS", true], ["16", "MODULES", false], ["5", "PERSONAS", false]].map(([num, label, hasSub]) => (
              <div key={label as string} style={{ textAlign: "center" }}>
                <div style={{ fontFamily: "Georgia, serif", fontSize: 52, color: "white" }}>{num as string}</div>
                <div style={{ fontFamily: "monospace", fontSize: 11, color: "#57606a", letterSpacing: 2 }}>{label as string}</div>
                {hasSub && (
                  <div style={{ fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 14, color: "#8b949e", marginTop: 6 }}>
                    The Data Centre Clock
                  </div>
                )}
              </div>
            ))}
          </div>
          <div style={{ opacity: fadeIn(frame, 1290), fontFamily: "monospace", fontSize: 15, color: "#8b949e", marginTop: 32 }}>
            Story teaches the why. Modules teach the how.
          </div>
          <div style={{ opacity: fadeIn(frame, 1335), fontFamily: "monospace", fontSize: 15, color: "#8b949e", marginTop: 8 }}>
            Irish standards. Irish grid. Irish deadlines.
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // ── SCENE 7: END SCREEN ──
  if (scene7) {
    const cloudRadius = 200;
    return (
      <AbsoluteFill style={{ backgroundColor: "#0a0e14" }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", position: "relative" }}>
          <div style={{ opacity: fadeIn(frame, 1380), fontFamily: "Georgia, serif", fontSize: 48, color: "white", textAlign: "center" }}>
            Three chapters. Three modules.
          </div>
          <div style={{ opacity: fadeIn(frame, 1440), fontFamily: "Georgia, serif", fontSize: 68, color: "#4a7c59", marginTop: 12 }}>
            Free.
          </div>
          <div style={{
            opacity: fadeIn(frame, 1500), marginTop: 24,
            width: 80, height: 80, borderRadius: "50%", overflow: "hidden",
            border: "2px solid #4a7c59",
            display: "flex", alignItems: "center", justifyContent: "center",
            background: "#0a0e14",
          }}>
            <Img src={staticFile("logo_only.png")} style={{ width: 100, height: 100, objectFit: "cover" }} />
          </div>
          <div style={{ opacity: fadeIn(frame, 1530), fontFamily: "Georgia, serif", fontWeight: "bold", fontSize: 42, color: "#4a7c59", marginTop: 12 }}>
            DC-LEARN
          </div>
          <div style={{ opacity: fadeIn(frame, 1545), fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 16, color: "#8b949e", marginTop: 8 }}>
            The convergence course for data centre professionals
          </div>

          {/* Word cloud */}
          <div style={{ opacity: fadeIn(frame, 1560), position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}>
            {LARGE_TERMS.map((t, i) => {
              const pos = clockPos(t.angle, cx, height / 2, cloudRadius + 60, cloudRadius + 20);
              return (
                <span key={t.text} style={{ position: "absolute", left: pos.x, top: pos.y, transform: "translate(-50%,-50%)", fontFamily: "monospace", fontSize: 18, color: t.color, opacity: 0.9 }}>
                  {t.text}
                </span>
              );
            })}
            {MEDIUM_TERMS.map((t, i) => {
              const a = (i / MEDIUM_TERMS.length) * 360 + 11;
              const pos = clockPos(a, cx, height / 2, cloudRadius + 140, cloudRadius + 100);
              return (
                <span key={t} style={{ position: "absolute", left: pos.x, top: pos.y, transform: "translate(-50%,-50%)", fontFamily: "monospace", fontSize: 13, color: "white", opacity: 0.55 }}>
                  {t}
                </span>
              );
            })}
            {SMALL_TERMS.map((t, i) => {
              const a = (i / SMALL_TERMS.length) * 360 + 7;
              const pos = clockPos(a, cx, height / 2, cloudRadius + 240, cloudRadius + 180);
              return (
                <span key={t} style={{ position: "absolute", left: pos.x, top: pos.y, transform: "translate(-50%,-50%)", fontFamily: "monospace", fontSize: 10, color: "white", opacity: 0.3 }}>
                  {t}
                </span>
              );
            })}
          </div>

          <div style={{ opacity: fadeIn(frame, 1590), position: "absolute", bottom: 40, fontFamily: "monospace", fontSize: 12, color: "#4a7c59" }}>
            legacybe.ie
          </div>
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

        {/* Building green text (4B) */}
        {frame >= 870 && (
          <>
            <div style={{ position: "absolute", left: "50%", top: 605, transform: "translateX(-50%)", opacity: fadeIn(frame, 890), fontFamily: "monospace", color: "#4a7c59", fontSize: 14, fontWeight: "bold", whiteSpace: "nowrap" }}>
              Understood. Aligned. Ahead of the clock.
            </div>
            <div style={{ position: "absolute", left: "50%", top: 625, transform: "translateX(-50%)", opacity: fadeIn(frame, 900), fontFamily: "monospace", color: "#57606a", fontSize: 11, whiteSpace: "nowrap" }}>
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

      {/* Connections SVG */}
      {frame >= 360 && frame < 930 && (
        <svg style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}>
          {CONNECTIONS.map((conn, i) => {
            if (frame < conn.start) return null;
            const isActive = activeConn === i;
            const lineOpacity = isActive ? 1 : 0.25;
            const path = connPath(conn.from, conn.to);
            return (
              <path key={i} d={path} fill="none" stroke="#c9d1d9" strokeWidth={isActive ? 2 : 1} opacity={lineOpacity} />
            );
          })}
        </svg>
      )}

      {/* Connection label */}
      {activeConn !== null && frame < 930 && (
        <div style={{ position: "absolute", bottom: 80, left: "50%", transform: "translateX(-50%)", backgroundColor: "rgba(10,14,20,0.85)", padding: "8px 16px", borderRadius: 20 }}>
          <div style={{ fontFamily: "monospace", fontStyle: "italic", fontSize: CONNECTIONS[activeConn].primary ? 15 : 13, color: "#c9d1d9", textAlign: "center", whiteSpace: "nowrap" }}>
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

      {/* Scene 5: Insight overlay */}
      {insightOverlay > 0 && (
        <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(10,14,20," + (0.88 * insightOverlay) + ")", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 24 }}>
          <div style={{ opacity: fadeIn(frame, 930), fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 44, color: "white", textAlign: "center", maxWidth: "80%" }}>
            They weren’t designed by the same people.
          </div>
          <div style={{ opacity: fadeIn(frame, 1005), fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 44, color: "white", textAlign: "center", maxWidth: "80%" }}>
            They weren’t drafted in the same year.
          </div>
          <div style={{ opacity: fadeIn(frame, 1080), fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 48, color: "#4a7c59", textAlign: "center", maxWidth: "80%" }}>
            But they all land on the same building, in the same decade.
          </div>
          <div style={{ opacity: fadeIn(frame, 1110), fontFamily: "monospace", fontSize: 13, color: "#57606a", textTransform: "uppercase", textAlign: "center", maxWidth: "80%", marginTop: 16 }}>
            Nobody coordinated them. But the deadlines coordinated themselves.
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
