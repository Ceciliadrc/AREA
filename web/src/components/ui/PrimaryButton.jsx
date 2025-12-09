/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** PrimaryButton.jsx
*/

import { colors, radius } from "../theme";

export default function PrimaryButton({
  children,
  onClick,
  fullWidth = true,
  style = {},
}) {
  return (
    <button
      onClick={onClick}
      style={{
        width: fullWidth ? "100%" : "auto",
        padding: "12px 24px",
        borderRadius: radius.pill,
        border: "none",
        cursor: "pointer",
        fontWeight: "bold",
        color: "#fff",
        background: colors.primaryGradient,
        fontSize: 15,
        ...style,
      }}
    >
      {children}
    </button>
  );
}
