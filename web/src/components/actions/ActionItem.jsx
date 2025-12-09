/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** ActionItem.jsx
*/

import OutlineCard from "../layout/OutlineCard";
import { colors } from "../theme";

export default function ActionItem({
  label,
  onClick,
  isAdd = false,
}) {
  return (
    <OutlineCard
      onClick={onClick}
      style={{
        textAlign: "center",
        paddingTop: 18,
        paddingBottom: 18,
        margin: "0 80px 16px",
      }}
    >
      <span
        style={{
          fontSize: isAdd ? 28 : 18,
          color: colors.textMain,
        }}
      >
        {label}
      </span>
    </OutlineCard>
  );
}
