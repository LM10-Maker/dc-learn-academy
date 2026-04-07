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

  // Building color transition: ramp up 885-920, hold 920-1050, ramp down 1050-1080
  const greenUp = interpolate(frame, [885, 920], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const greenDown = interpolate(frame, [1050, 1080], [1, 0], {
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
  const insightOverlay = frame >= 1080 && frame < 1290 ? fadeIn(frame, 1080, 20) : 0;
  const clockDim = frame >= 1095 ? 0 : frame >= 1080 ? 0.15 : 1;
  const scene6 = frame >= 1290 && frame < 1440;
  const scene7 = frame >= 1440;

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
          opacity: fadeIn(frame, 1290),
          fontFamily: "monospace", color: "#4a7c59", fontSize: 14,
          textTransform: "uppercase", letterSpacing: 4,
        }}>
          DC-LEARN
        </div>

        {/* Headline */}
        <div style={{
          position: "absolute", left: "50%", top: 350, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1305, 18),
          fontFamily: "Georgia, serif", fontSize: 46, color: "white",
          textAlign: "center", maxWidth: 900, lineHeight: 1.2,
        }}>
          The only learning resource that shows how they connect.
        </div>

        {/* Three stat columns */}
        <div style={{
          position: "absolute", left: "50%", top: 480, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1350),
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
          opacity: fadeIn(frame, 1395),
          fontFamily: "monospace", fontSize: 15, color: "#8b949e", textAlign: "center",
        }}>
          Story teaches the why. Modules teach the how.
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 640, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1410),
          fontFamily: "monospace", fontSize: 15, color: "#8b949e", textAlign: "center",
        }}>
          Irish standards. Irish grid. Irish deadlines.
        </div>
      </AbsoluteFill>
    );
  }

  // ── SCENE 7: END SCREEN — static word cloud in four zones ──
  if (scene7) {
    const wcOp = fadeIn(frame, 1620, 30); // word cloud fade-in

    return (
      <AbsoluteFill style={{ backgroundColor: "#0a0e14" }}>
        {/* PHASE 1: CTA text */}
        <div style={{
          position: "absolute", left: "50%", top: 440, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1440),
          fontFamily: "Georgia, serif", fontSize: 48, color: "white", textAlign: "center",
        }}>
          Three chapters. Three modules.
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 520, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1500),
          fontFamily: "Georgia, serif", fontSize: 68, color: "#4a7c59",
        }}>
          Free.
        </div>

        {/* PHASE 2: Logo + branding */}
        <div style={{
          position: "absolute", left: "50%", top: 620, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1560),
          width: 100, height: 100, borderRadius: "50%", overflow: "hidden",
          border: "2px solid #4a7c59",
          display: "flex", alignItems: "center", justifyContent: "center",
          background: "#0a0e14",
        }}>
          <Img src={staticFile("logo_only.png")} style={{ width: 120, height: 120, objectFit: "cover" }} />
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 730, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1590),
          fontFamily: "Georgia, serif", fontWeight: "bold", fontSize: 42, color: "#4a7c59",
        }}>
          DC-LEARN
        </div>
        <div style={{
          position: "absolute", left: "50%", top: 765, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1605),
          fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 16, color: "#8b949e",
        }}>
          The convergence course for data centre professionals
        </div>

        {/* ZONE 1 — TOP STRIP (y=50-250, full width) */}
        {([
          { text: "IS 10101", x: 80, y: 65, color: "#5B9BD5" }, { text: "redundancy", x: 350, y: 65, color: "#8DB4C8" }, { text: "CIBSE TM40", x: 620, y: 65, color: "#5B9BD5" }, { text: "GHG Protocol", x: 1000, y: 65, color: "#2dd4bf" }, { text: "topology", x: 1300, y: 65, color: "#8DB4C8" }, { text: "SLA", x: 1550, y: 65, color: "#8DB4C8" }, { text: "dry coolers", x: 1720, y: 65, color: "#5B9BD5" },
          { text: "EN 50600", x: 120, y: 115, color: "#5B9BD5" }, { text: "ATS", x: 380, y: 115, color: "#D4A84B" }, { text: "concurrent maintainability", x: 680, y: 115, color: "#e879a0" }, { text: "NEAP", x: 1050, y: 115, color: "#4a7c59" }, { text: "DCIM", x: 1300, y: 115, color: "#8DB4C8" }, { text: "BMS", x: 1500, y: 115, color: "#8DB4C8" }, { text: "EPO", x: 1750, y: 115, color: "#C75050" },
          { text: "N+1", x: 160, y: 165, color: "#D4A84B" }, { text: "chillers", x: 400, y: 165, color: "#5B9BD5" }, { text: "Scope 2 market-based", x: 700, y: 165, color: "#2dd4bf" }, { text: "48-hour fuel", x: 1100, y: 165, color: "#C75050" }, { text: "PDU whip", x: 1400, y: 165, color: "#D4A84B" }, { text: "EN 61439", x: 1700, y: 165, color: "#5B9BD5" },
          { text: "delta-T", x: 100, y: 215, color: "#5B9BD5" }, { text: "BESS", x: 350, y: 215, color: "#4a7c59" }, { text: "discrimination study", x: 620, y: 215, color: "#8DB4C8" }, { text: "additionality", x: 1000, y: 215, color: "#2dd4bf" }, { text: "thermal runaway", x: 1350, y: 215, color: "#C75050" }, { text: "HV switchgear", x: 1680, y: 215, color: "#D4A84B" },
        ] as const).map((t) => (
          <span key={t.text + t.x} style={{
            position: "absolute", left: t.x, top: t.y,
            fontFamily: "monospace", fontSize: 20, color: t.color, opacity: 0.55 * wcOp,
          }}>
            {t.text}
          </span>
        ))}

        {/* ZONE 2 — LEFT COLUMN (x=40-420, y=280-950) */}
        {([
          { text: "PUE", x: 60, y: 300, size: 22, color: "#D4A84B", op: 0.75 },
          { text: "2N+1", x: 200, y: 330, size: 20, color: "#D4A84B", op: 0.55 },
          { text: "F-Gas", x: 40, y: 360, size: 22, color: "#E06060", op: 0.75 },
          { text: "fault tolerance", x: 180, y: 390, size: 20, color: "#e879a0", op: 0.55 },
          { text: "CRREM", x: 80, y: 420, size: 22, color: "#e879a0", op: 0.75 },
          { text: "static transfer", x: 220, y: 450, size: 20, color: "#D4A84B", op: 0.55 },
          { text: "containment", x: 50, y: 480, size: 20, color: "#8DB4C8", op: 0.55 },
          { text: "busway", x: 250, y: 510, size: 20, color: "#8DB4C8", op: 0.55 },
          { text: "delta-T", x: 100, y: 540, size: 20, color: "#5B9BD5", op: 0.55 },
          { text: "rack PDU", x: 200, y: 570, size: 20, color: "#D4A84B", op: 0.55 },
          { text: "VESDA", x: 60, y: 600, size: 20, color: "#C75050", op: 0.55 },
          { text: "ASHRAE", x: 280, y: 630, size: 20, color: "#5B9BD5", op: 0.55 },
          { text: "HVO", x: 40, y: 660, size: 20, color: "#4a7c59", op: 0.55 },
          { text: "hot aisle", x: 220, y: 690, size: 20, color: "#C75050", op: 0.55 },
          { text: "WAULT", x: 80, y: 720, size: 20, color: "#e879a0", op: 0.55 },
          { text: "€/kW", x: 50, y: 780, size: 20, color: "#fb923c", op: 0.55 },
          { text: "lifecycle cost", x: 40, y: 840, size: 20, color: "#8DB4C8", op: 0.55 },
          { text: "Icw rating", x: 70, y: 900, size: 20, color: "#D4A84B", op: 0.55 },
        ] as const).map((t) => (
          <span key={t.text + t.x} style={{
            position: "absolute", left: t.x, top: t.y,
            fontFamily: "monospace", fontSize: t.size, color: t.color, opacity: t.op * wcOp,
          }}>
            {t.text}
          </span>
        ))}

        {/* ZONE 3 — RIGHT COLUMN (x=1100-1880, y=280-950) */}
        {([
          { text: "CRU", x: 1600, y: 300, size: 22, color: "#4a7c59", op: 0.75 },
          { text: "dual feed", x: 1150, y: 330, size: 20, color: "#D4A84B", op: 0.55 },
          { text: "EED", x: 1720, y: 360, size: 22, color: "#5B9BD5", op: 0.75 },
          { text: "power quality", x: 1120, y: 390, size: 20, color: "#8DB4C8", op: 0.55 },
          { text: "Carbon Tax", x: 1540, y: 420, size: 22, color: "#fb923c", op: 0.75 },
          { text: "HV protection", x: 1180, y: 450, size: 20, color: "#C75050", op: 0.55 },
          { text: "Grid", x: 1680, y: 480, size: 22, color: "#a78bfa", op: 0.75 },
          { text: "chilled water", x: 1140, y: 510, size: 20, color: "#5B9BD5", op: 0.55 },
          { text: "free cooling", x: 1560, y: 540, size: 20, color: "#5B9BD5", op: 0.55 },
          { text: "condenser", x: 1200, y: 570, size: 20, color: "#5B9BD5", op: 0.55 },
          { text: "MIC", x: 1720, y: 600, size: 20, color: "#D4A84B", op: 0.55 },
          { text: "Li-ion", x: 1160, y: 630, size: 20, color: "#fb923c", op: 0.55 },
          { text: "Novec 1230", x: 1540, y: 660, size: 20, color: "#C75050", op: 0.55 },
          { text: "EPA licence", x: 1120, y: 690, size: 20, color: "#4a7c59", op: 0.55 },
          { text: "CDU", x: 1700, y: 720, size: 20, color: "#5B9BD5", op: 0.55 },
          { text: "cap rate", x: 1560, y: 780, size: 20, color: "#fb923c", op: 0.55 },
          { text: "elemental cost plan", x: 1520, y: 840, size: 20, color: "#8DB4C8", op: 0.55 },
          { text: "Fire", x: 1680, y: 900, size: 22, color: "#C75050", op: 0.75 },
        ] as const).map((t) => (
          <span key={t.text + t.x} style={{
            position: "absolute", left: t.x, top: t.y,
            fontFamily: "monospace", fontSize: t.size, color: t.color, opacity: t.op * wcOp,
          }}>
            {t.text}
          </span>
        ))}

        {/* ZONE 4 — BOTTOM (x=450-1450, y=760-940) */}
        {([
          { text: "discrimination study", x: 480, y: 760, color: "#8DB4C8" },
          { text: "additionality", x: 780, y: 760, color: "#2dd4bf" },
          { text: "GHG Protocol", x: 1050, y: 760, color: "#2dd4bf" },
          { text: "PDU", x: 1300, y: 760, color: "#D4A84B" },
          { text: "Scope 2", x: 480, y: 810, color: "#2dd4bf" },
          { text: "commissioning", x: 750, y: 810, color: "#4a7c59" },
          { text: "48-hour fuel", x: 1050, y: 810, color: "#C75050" },
          { text: "UPS", x: 1300, y: 810, color: "#D4A84B" },
          { text: "server PSU", x: 480, y: 840, color: "#D4A84B" },
          { text: "heat rejection", x: 720, y: 840, color: "#C75050" },
          { text: "uptime tier", x: 1000, y: 840, color: "#e879a0" },
          { text: "PPA", x: 1250, y: 840, color: "#4a7c59" },
          { text: "witness testing", x: 550, y: 890, color: "#8DB4C8" },
          { text: "point-to-point", x: 850, y: 890, color: "#5B9BD5" },
        ] as const).map((t) => (
          <span key={t.text + t.x} style={{
            position: "absolute", left: t.x, top: t.y,
            fontFamily: "monospace", fontSize: 20, color: t.color, opacity: 0.55 * wcOp,
          }}>
            {t.text}
          </span>
        ))}

        {/* legacybe.ie */}
        <div style={{
          position: "absolute", left: "50%", top: 980, transform: "translate(-50%, -50%)",
          opacity: fadeIn(frame, 1650),
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
          {frame >= 885 && frame < 1080 ? "400 racks · 2.4 MW · PUE 1.30 · Retrofitting" : "400 racks · 2.4 MW · PUE 1.50 · Built 2013"}
        </div>


        {/* 4B setup text — fades in at 870, out at 1050-1080 */}
        {frame >= 870 && frame < 1080 && (
          <div style={{
            position: "absolute", left: "50%", top: 445, transform: "translateX(-50%)",
            opacity: fadeIn(frame, 870) * (1 - fadeIn(frame, 1050, 30)),
            fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 18, color: "#8b949e", whiteSpace: "nowrap",
          }}>
            When you understand the connections...
          </div>
        )}

        {/* Building green text (4B) — visible during green hold, fades out 1050-1080 */}
        {frame >= 920 && frame < 1080 && (
          <>
            <div style={{ position: "absolute", left: "50%", top: 575, transform: "translateX(-50%)", opacity: fadeIn(frame, 920) * (1 - fadeIn(frame, 1050, 30)), fontFamily: "monospace", color: "#4a7c59", fontSize: 20, fontWeight: "bold", whiteSpace: "nowrap" }}>
              Understood. Aligned. Ahead of the clock.
            </div>
            <div style={{ position: "absolute", left: "50%", top: 600, transform: "translateX(-50%)", opacity: fadeIn(frame, 920) * (1 - fadeIn(frame, 1050, 30)), fontFamily: "monospace", color: "#8b949e", fontSize: 14, whiteSpace: "nowrap" }}>
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
      {frame >= 360 && frame < 1050 && (
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

      {/* Connection label — pill at y=630, inside clock ring */}
      {activeConn !== null && frame < 870 && (
        <div style={{
          position: "absolute", left: "50%", top: 630, transform: "translate(-50%, -50%)",
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
            { text: "They weren’t designed by the same people.", start: 1095, y: 400, size: 44, color: "white", font: "Georgia, serif", style: "italic" as const },
            { text: "They weren’t drafted in the same year.", start: 1170, y: 460, size: 44, color: "white", font: "Georgia, serif", style: "italic" as const },
            { text: "But they all land on the same building, in the same decade.", start: 1230, y: 530, size: 48, color: "#4a7c59", font: "Georgia, serif", style: "italic" as const },
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
            const op4 = fadeIn(frame, 1260);
            const ty4 = interpolate(frame, [1260, 1275], [12, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
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
