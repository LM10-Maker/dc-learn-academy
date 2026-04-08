import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Img, staticFile } from "remotion";
import "@fontsource/playfair-display/400.css";
import "@fontsource/playfair-display/400-italic.css";
import "@fontsource/ibm-plex-mono/400.css";

const playfair = { fontFamily: "'Playfair Display'" };
const plexMono = { fontFamily: "'IBM Plex Mono'" };

export const DCLearnLoop: React.FC = () => {
  const frame = useCurrentFrame();

  const logoOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const textOpacity = interpolate(frame, [20, 50], [0, 1], { extrapolateRight: "clamp" });
  const pulseScale = 1 + 0.02 * Math.sin(frame * 0.1);

  const fadeOut = interpolate(frame, [315, 345], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e14", opacity: fadeOut }}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
          gap: 20,
        }}
      >
        <div
          style={{
            opacity: logoOpacity,
            transform: `scale(${pulseScale})`,
            width: 100,
            height: 100,
            borderRadius: "50%",
            border: "2px solid #4a7c59",
            overflow: "hidden",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Img src={staticFile("logo_only.png")} style={{ width: 80 }} />
        </div>
        <div
          style={{
            opacity: textOpacity,
            fontFamily: plexMono.fontFamily,
            color: "#4a7c59",
            fontSize: 24,
            letterSpacing: 6,
            textTransform: "uppercase",
          }}
        >
          DC-LEARN
        </div>
        <div
          style={{
            opacity: textOpacity,
            fontFamily: playfair.fontFamily,
            fontStyle: "italic",
            color: "#8b949e",
            fontSize: 16,
          }}
        >
          The convergence course for data centre professionals
        </div>
      </div>
    </AbsoluteFill>
  );
};
