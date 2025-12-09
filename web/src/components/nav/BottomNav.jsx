/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** BottomNav.jsx
*/

import { colors, radius } from "../theme";
import IconList from "../../assets/list.png";
import IconAdd from "../../assets/plus.png";
import IconProfile from "../../assets/icon.png";

export default function BottomNav({ active = "list", onNavigate }) {
  const tabs = [
    { id: "list", icon: IconList },
    { id: "create", icon: IconAdd },
    { id: "profile", icon: IconProfile },
  ];

  return (
    <div
      style={{
        position: "fixed",
        left: "50%",
        bottom: 32,
        transform: "translateX(-50%)",
        backgroundColor: colors.primaryDark,
        padding: 8,
        borderRadius: radius.pill,
        display: "flex",
        gap: 8,
      }}
    >
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onNavigate(tab.id)}
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            padding: "8px 14px",
            borderRadius: radius.pill,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: active === tab.id ? 1 : 0.7,
          }}
        >
          <img
            src={tab.icon}
            alt={tab.id}
            style={{ width: 22, height: 22 }}
          />
        </button>
      ))}
    </div>
  );
}
