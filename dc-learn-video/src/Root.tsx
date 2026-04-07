import React from "react";
import { Composition } from "remotion";
import { DCLearnConvergence } from "./DCLearnConvergence";
import { DCLearnLoop } from "./DCLearnLoop";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="DCLearnConvergence"
        component={DCLearnConvergence}
        durationInFrames={1800}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="DCLearnConvergenceSocial"
        component={DCLearnConvergence}
        durationInFrames={1800}
        fps={30}
        width={1080}
        height={1080}
      />
      <Composition
        id="DCLearnLoop"
        component={DCLearnLoop}
        durationInFrames={345}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
