/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** PageTitle.jsx
*/

import { colors } from "../theme";

export function PageTitle({ children }) {
  return (
    <h1
      style={{
        textAlign: "center",
        marginTop: 40,
        marginBottom: 16,
        fontSize: 40,
        fontWeight: 600,
        color: colors.textMain,
      }}
    >
      {children}
    </h1>
  );
}

export function PageSubtitle({ children }) {
  return (
    <p
      style={{
        textAlign: "center",
        margin: 0,
        marginBottom: 24,
        fontSize: 20,
        color: colors.textMuted,
      }}
    >
      {children}
    </p>
  );
}
