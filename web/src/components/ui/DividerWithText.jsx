/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** DividerWithText.jsx
*/

import { colors } from "../theme";

export default function DividerWithText({ children = "or" }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 8,
        marginTop: 24,
        marginBottom: 8,
        fontSize: 12,
        color: colors.textMuted,
      }}
    >
      <div style={{ flex: 1, height: 1, backgroundColor: "#ddd" }} />
      <span>{children}</span>
      <div style={{ flex: 1, height: 1, backgroundColor: "#ddd" }} />
    </div>
  );
}
