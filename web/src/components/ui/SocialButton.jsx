/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** SocialButton.jsx
*/

import { colors, radius } from "../theme";

export default function SocialButton({
  iconSrc,
  alt,
  onClick,
  href,
}) {
  const handleClick = () => {
    if (href) {
      window.open(href, "_blank");
    } else if (onClick) {
      onClick();
    }
  };

  return (
    <button
      onClick={handleClick}
      style={{
        flex: 1,
        padding: "8px 0",
        borderRadius: radius.card,
        border: `1px solid ${colors.border}`,
        backgroundColor: "#fff",
        cursor: "pointer",
      }}
    >
      <img
        src={iconSrc}
        alt={alt}
        style={{ height: 22, pointerEvents: "none" }}
      />
    </button>
  );
}
