/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** TextButton.jsx
*/

import { colors } from "../theme";

export default function TextButton({
  children,
  onClick,
  style = {},
}) {
  return (
    <button
      onClick={onClick}
      style={{
        border: "none",
        background: "none",
        color: colors.primary,
        cursor: "pointer",
        fontSize: 13,
        padding: 0,
        ...style,
      }}
    >
      {children}
    </button>
  );
}
