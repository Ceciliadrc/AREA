/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** OutlineCard.jsx
*/

import { colors, radius } from "../theme";

export default function OutlineCard({
  children,
  onClick,
  style = {},
}) {
  return (
    <div
      onClick={onClick}
      style={{
        border: `2px solid ${colors.border}`,
        borderRadius: radius.card,
        padding: "18px 24px",
        backgroundColor: "transparent",
        cursor: onClick ? "pointer" : "default",
        ...style,
      }}
    >
      {children}
    </div>
  );
}
