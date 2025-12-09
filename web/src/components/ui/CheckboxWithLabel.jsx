/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** CheckboxWithLabel.jsx
*/

import { colors } from "../theme";

export default function CheckboxWithLabel({
  label,
  checked,
  onChange,
}) {
  return (
    <label
      style={{
        fontSize: 13,
        color: colors.textMain,
        display: "flex",
        alignItems: "center",
        gap: 6,
      }}
    >
      <input
        type="checkbox"
        checked={checked}
        onChange={onChange}
        style={{ accentColor: colors.primary }}
        background-color="white"
      />
      {label}
    </label>
  );
}
