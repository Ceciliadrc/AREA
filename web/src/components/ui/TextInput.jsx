/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** TextInput.jsx
*/

import { colors } from "../theme";

export default function TextInput({
  label,
  type = "text",
  placeholder = "",
  style = {},
  ...rest
}) {
  return (
    <div style={{ marginBottom: 16 }}>
      {label && (
        <label
          style={{
            fontSize: 14,
            display: "block",
            marginBottom: 6,
            color: colors.textMain,
          }}
        >
          {label}
        </label>
      )}
      <input
        type={type}
        placeholder={placeholder}
        style={{
          width: "100%",
          padding: "10px 12px",
          borderRadius: 10,
          border: `1px solid ${colors.border}`,
          outline: "none",
          fontSize: 14,
          color: colors.textMain,
          ...style,
        }}
        {...rest}
      />
    </div>
  );
}
