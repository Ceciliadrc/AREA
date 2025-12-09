/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** CenteredCardLayout.jsx
*/

import { colors, radius } from "../theme";

export default function CenteredCardLayout({ children, width = 380 }) {
  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100vw",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: colors.bgGradient,
      }}
    >
      <div
        style={{
          backgroundColor: colors.cardBg,
          width,
          padding: "32px 40px",
          borderRadius: radius.card,
          boxShadow: "0 20px 40px rgba(0,0,0,0.15)",
        }}
      >
        {children}
      </div>
    </div>
  );
}
