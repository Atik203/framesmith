import React from "react";
import {
  AbsoluteFill,
  Audio,
  Composition,
  Img,
  Sequence,
  staticFile,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import spec from "../../v1/renders/lf-short-001.spec.json";
import subtitles from "../../v1/subtitles/lf-short-001.json";

type Scene = (typeof spec.scenes)[number];
type Caption = (typeof subtitles.chunks)[number];

const SceneImage: React.FC<{ scene: Scene; index: number }> = ({ scene, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const duration = Math.max(1, Math.round(scene.duration * fps));
  const progress = interpolate(frame, [0, duration], [0, 1], {
    extrapolateRight: "clamp",
  });
  const direction = index % 2 === 0 ? 1 : -1;
  const scale = scene.motion === "push_out" ? 1.12 - progress * 0.08 : 1.02 + progress * 0.08;
  const translateX = scene.motion.startsWith("pan") ? direction * progress * 28 : 0;
  const filename = scene.asset.slice(scene.asset.lastIndexOf("/") + 1);
  const source = `lf-short-001/${filename}`;

  return (
    <AbsoluteFill style={{ backgroundColor: "#10151b", overflow: "hidden" }}>
      <Img
        src={staticFile(source)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          filter: "blur(24px) brightness(0.38)",
          transform: `scale(1.16)`,
        }}
      />
      <Img
        src={staticFile(source)}
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          objectFit: "contain",
          transform: `translateX(${translateX}px) scale(${scale})`,
        }}
      />
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(4,8,13,.08) 45%, rgba(4,8,13,.68) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nowMs = (frame / fps) * 1000;
  const active = (subtitles.chunks as Caption[]).find(
    (caption) => nowMs >= caption.start * 1000 && nowMs < caption.end * 1000,
  );
  if (!active) return null;

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", padding: "0 88px 290px" }}>
      <div
        style={{
          maxWidth: 920,
          color: "#fff8e9",
          fontFamily: '"Segoe UI", sans-serif',
          fontWeight: 800,
          fontSize: 62,
          lineHeight: 1.12,
          textAlign: "center",
          textShadow: "0 3px 10px #000, 0 0 4px #000",
          letterSpacing: 0.2,
        }}
      >
        {active.text}
      </div>
    </AbsoluteFill>
  );
};

const ShortVideo: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: "#10151b" }}>
      {spec.scenes.map((scene, index) => (
        <Sequence
          key={`${scene.asset}-${index}`}
          from={Math.round(scene.start * fps)}
          durationInFrames={Math.round(scene.duration * fps)}
        >
          <SceneImage scene={scene} index={index} />
        </Sequence>
      ))}
      <Audio src={staticFile("lf-short-001/lf-short-001.wav")} />
      <Captions />
    </AbsoluteFill>
  );
};

export const MyComposition = () => (
  <Composition
    id="ShortVertical"
    component={ShortVideo}
    durationInFrames={Math.ceil(spec.duration_seconds * spec.fps)}
    fps={spec.fps}
    width={spec.width}
    height={spec.height}
  />
);
