/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** ProfilePicture.jsx
*/

import { colors } from "../theme";

export default function ProfilePicture({
  size = 160,
  background = colors.primary,
}) {
  const iconSize = size * 0.45;

  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: "50%",
        backgroundColor: background,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <svg
        width={iconSize}
        height={iconSize}
        viewBox="0 0 48 48"
        fill="none"
      >
        <circle
          cx="24"
          cy="18"
          r="8"
          stroke="white"
          strokeWidth="2.5"
        />
        <path
          d="M10 38C12.5 31.5 17.75 28 24 28C30.25 28 35.5 31.5 38 38"
          stroke="white"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
}
