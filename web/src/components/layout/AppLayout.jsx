/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** AppLayout.jsx
*/

import { colors } from "../theme";

export default function AppLayout({ children }) {
  return (
    <div
      style={{
        minHeight: "100vh",
        minWidth: "562px",
        width: "100vw",
        backgroundColor: colors.appBg,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {children}
    </div>
  );
}
