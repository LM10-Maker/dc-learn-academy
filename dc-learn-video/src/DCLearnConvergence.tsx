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
    case "steady": return (frame / 720) * 360;
    case "counter": return -(frame / 720) * 360;
    case "stuck": return 144;
    case "fast": return (frame / 360) * 360;
    case "accelerating": return (frame * frame * 0.001) / 3;
    case "frozen": return 0;
    case "redRing": return (frame / 720) * 360;
    case "pulse": return (frame / 720) * 360;
    default: return (frame / 720) * 360;
  }
};

// ── Component ─────────────────────────────────────────
export const DCLearnConvergence: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const cx = 960;
  const cy = 520;
  const ringRadius = 420;

  // Building color transition: ramp up 885-920, hold 920-1110, ramp down 1110-1140
  const greenUp = interpolate(frame, [885, 920], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const greenDown = interpolate(frame, [1110, 1140], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const greenT = Math.min(greenUp, greenDown);
  const rackStroke = interpolateColors(greenT, [0, 1], ["#3d444d", "#4a7c59"]);
  const rackFill = interpolateColors(greenT, [0, 1], ["#1c2128", "rgba(74,124,89,0.15)"]);
  const outlineStroke = interpolateColors(greenT, [0, 1], ["#3d444d", "#4a7c59"]);

  // Scene visibility
  const openingOpacity = fadeIn(frame, 15, 30);
  const clocksVisible = frame >= 90;
  const insightOverlay = frame >= 1200 && frame < 1410 ? fadeIn(frame, 1200, 20) : 0;
  const clockDim = frame >= 1215 ? 0 : frame >= 1200 ? 0.15 : 1;
  const scene6 = frame >= 1410 && frame < 1590;
  const scene7 = frame >= 1590;

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
          position: "absolute", left: "50%", top: 250, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1410),
          fontFamily: "monospace", color: "#4a7c59", fontSize: 14,
          textTransform: "uppercase", letterSpacing: 4,
        }}>
          DC-LEARN
        </div>

        {/* Headline */}
        <div style={{
          position: "absolute", left: "50%", top: 350, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1430, 18),
          fontFamily: "Georgia, serif", fontSize: 46, color: "white",
          textAlign: "center", maxWidth: 900, lineHeight: 1.2,
        }}>
          The only learning resource that shows how they connect.
        </div>

        {/* Three stat columns */}
        <div style={{
          position: "absolute", left: "50%", top: 480, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1490),
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
          opacity: fadeIn(frame, 1540),
          fontFamily: "monospace", fontSize: 15, color: "#8b949e", textAlign: "center",
        }}>
          Story teaches the why. Modules teach the how.
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 640, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1565),
          fontFamily: "monospace", fontSize: 15, color: "#8b949e", textAlign: "center",
        }}>
          Irish standards. Irish grid. Irish deadlines.
        </div>
      </AbsoluteFill>
    );
  }

  // ── SCENE 7: END SCREEN — clean, six elements only ──
  if (scene7) {
    return (
      <AbsoluteFill style={{ backgroundColor: "#0a0e14" }}>
        <div style={{
          position: "absolute", left: "50%", top: 340, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1590),
          fontFamily: "Georgia, serif", fontSize: 48, color: "white", textAlign: "center",
        }}>
          Three chapters. Three modules.
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 420, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1650),
          fontFamily: "Georgia, serif", fontSize: 68, color: "#4a7c59",
        }}>
          Free.
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 500, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1700),
          width: 100, height: 100, borderRadius: "50%", overflow: "hidden",
          border: "2px solid #4a7c59",
          display: "flex", alignItems: "center", justifyContent: "center",
          background: "#0a0e14",
        }}>
          <Img src={staticFile("logo_only.png")} style={{ width: 120, height: 120, objectFit: "cover" }} />
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 620, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1730),
          fontFamily: "Georgia, serif", fontWeight: "bold", fontSize: 42, color: "#4a7c59",
        }}>
          DC-LEARN
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 660, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1745),
          fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 16, color: "#8b949e",
        }}>
          The convergence course for data centre professionals
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 980, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1760),
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

        {/* Stats at y=555 — text and colour change during green (885-1080) */}
        <div style={{
          position: "absolute", left: "50%", top: 555, transform: "translateX(-50%)",
          fontFamily: "monospace", fontSize: 13, whiteSpace: "nowrap",
          color: interpolateColors(greenT, [0, 1], ["#57606a", "#4a7c59"]),
        }}>
          {frame >= 885 && frame < 1140 ? "400 racks · 2.4 MW · PUE 1.30 · Retrofitting" : "400 racks · 2.4 MW · PUE 1.50 · Built 2013"}
        </div>


        {/* 4B setup text — fades in at 870, out at 1110-1140, prominent */}
        {frame >= 870 && frame < 1140 && (() => {
          const setupOp = fadeIn(frame, 870) * (1 - fadeIn(frame, 1110, 30));
          return (
            <>
              <div style={{
                position: "absolute", left: "50%", top: 446, transform: "translateX(-50%)",
                opacity: setupOp * 0.3,
                fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 24, color: "#4a7c59", whiteSpace: "nowrap",
              }}>
                When you understand the connections...
              </div>
              <div style={{
                position: "absolute", left: "50%", top: 445, transform: "translateX(-50%)",
                opacity: setupOp,
                fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 24, color: "#ffffff", whiteSpace: "nowrap",
              }}>
                When you understand the connections...
              </div>
            </>
          );
        })()}

        {/* Building green text (4B) — visible during green hold, fades out 1110-1140 */}
        {frame >= 920 && frame < 1140 && (
          <>
            <div style={{ position: "absolute", left: "50%", top: 575, transform: "translateX(-50%)", opacity: fadeIn(frame, 920) * (1 - fadeIn(frame, 1110, 30)), fontFamily: "monospace", color: "#4a7c59", fontSize: 20, fontWeight: "bold", whiteSpace: "nowrap" }}>
              Understood. Aligned. Ahead of the clock.
            </div>
            <div style={{ position: "absolute", left: "50%", top: 600, transform: "translateX(-50%)", opacity: fadeIn(frame, 920) * (1 - fadeIn(frame, 1110, 30)), fontFamily: "monospace", color: "#8b949e", fontSize: 14, whiteSpace: "nowrap" }}>
              The building that understands what’s coming.
            </div>
          </>
        )}
        {/* Grey hold text — after green fades, before insight */}
        {frame >= 1140 && frame < 1200 && (
          <div style={{
            position: "absolute", left: "50%", top: 620, transform: "translateX(-50%)",
            opacity: fadeIn(frame, 1140) * (1 - fadeIn(frame, 1185, 15)),
            fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 18, color: "#8b949e", whiteSpace: "nowrap",
          }}>
            Retrofit starts with understanding.
          </div>
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

            // No pulse blink — clocks stay fully visible
            const pulseOp = 1;

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
                  <text x={labelX} y={labelY + 16} textAnchor={textAnchor} fill={clock.color} fontFamily="monospace" fontSize={13} opacity={0.8}>
                    {clock.stat}
                  </text>
                </g>
              </g>
            );
          })}
        </svg>
      )}

      {/* Connections SVG — dashed, animated, perimeter-to-perimeter */}
      {frame >= 360 && frame < 1110 && (
        <svg style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}>
          {CONNECTIONS.map((conn, i) => {
            if (frame < conn.start) return null;
            const isActive = activeConn === i;
            const lineOpacity = isActive ? 0.7 : 0.15;
            const path = connPath(conn.from, conn.to);
            const lineColor = CLOCKS[conn.from].color;
            return (
              <path
                key={i}
                d={path}
                fill="none"
                stroke={lineColor}
                strokeWidth={isActive ? 2 : 1.5}
                opacity={lineOpacity}
                strokeDasharray="8 6"
                strokeDashoffset={-(frame * 1.2)}
              />
            );
          })}
        </svg>
      )}

      {/* Connection label — pill at y=630, all 18px monospace italic */}
      {activeConn !== null && (
        <div style={{
          position: "absolute", left: "50%", top: 630, transform: "translate(-50%, -50%)",
          backgroundColor: "#0a0e14",
          border: "1px solid " + CLOCKS[CONNECTIONS[activeConn].from].color + "4d",
          padding: "10px 24px", borderRadius: 8,
        }}>
          <div style={{
            fontFamily: "monospace", fontStyle: "italic",
            fontSize: 18,
            color: "#c9d1d9", textAlign: "center", whiteSpace: "nowrap",
          }}>
            {CONNECTIONS[activeConn].label}
          </div>
        </div>
      )}

      {/* Scene 3 overlay text — at y=620 between building and bottom clocks */}
      {frame >= 300 && frame < 360 && (
        <div style={{ position: "absolute", left: "50%", top: 620, transform: "translate(-50%, -50%)", opacity: fadeIn(frame, 300) }}>
          <div style={{ fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 36, color: "rgba(255,255,255,0.7)", textAlign: "center", whiteSpace: "nowrap" }}>
            Eight regulations. One building. All ticking.
          </div>
        </div>
      )}

      {/* Scene 5: Insight overlay — absolute positioned, translateY entrance */}
      {insightOverlay > 0 && (
        <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(10,14,20," + (0.97 * insightOverlay) + ")" }}>
          {[
            { text: "They weren’t designed by the same people.", start: 1215, y: 400, size: 44, color: "white", font: "Georgia, serif", style: "italic" as const },
            { text: "They weren’t drafted in the same year.", start: 1290, y: 460, size: 44, color: "white", font: "Georgia, serif", style: "italic" as const },
            { text: "But they all land on the same building, in the same decade.", start: 1350, y: 530, size: 48, color: "#4a7c59", font: "Georgia, serif", style: "italic" as const },
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
            const op4 = fadeIn(frame, 1380);
            const ty4 = interpolate(frame, [1380, 1395], [12, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
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
