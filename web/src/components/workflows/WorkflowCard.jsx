/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** WorkflowCard.jsx
*/

import OutlineCard from "../layout/OutlineCard";
import { colors } from "../theme";

export default function WorkflowCard({
  title,
  description,
  onEdit,
}) {
  return (
    <OutlineCard
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        marginBottom: 24,
      }}
    >
      <div>
        <div
          style={{
            fontWeight: 600,
            fontSize: 20,
            marginBottom: 4,
            color: colors.textMain,
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontSize: 14,
            color: colors.textMuted,
          }}
        >
          {description}
        </div>
      </div>
      <button
        onClick={onEdit}
        style={{
          border: "none",
          background: "none",
          cursor: "pointer",
          fontSize: 18,
          color: colors.textMuted,
          marginLeft: 16,
        }}
      >
        ✏️
      </button>
    </OutlineCard>
  );
}
