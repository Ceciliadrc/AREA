/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** CredentialCard.jsx
*/

import OutlineCard from "../layout/OutlineCard";
import { colors } from "../theme";
import PlusRose from "../../assets/plus_rose.png";
import PenRose from "../../assets/pen_rose.png";

export default function CredentialCard({
  label,
  onClick,
  onEdit,
  isAdd = false,
}) {
  return (
    <OutlineCard
      onClick={onClick}
      style={{
        width: "100%",
        padding: "18px 24px",
        boxSizing: "border-box",
        display: "flex",
        alignItems: "center",
        justifyContent: isAdd ? "center" : "space-between",
        cursor: "pointer",
      }}
    >
      {isAdd ? (
        <img
          src={PlusRose}
          alt="Add credential"
          style={{ width: 22, height: 22 }}
        />
      ) : (
        <>
          <span
            style={{
              fontSize: 16,
              fontWeight: 600,
              color: colors.textMain,
            }}
          >
            {label}
          </span>

          {onEdit && (
            <span
              onClick={(e) => {
                e.stopPropagation();
                onEdit();
              }}
              style={{ display: "flex", alignItems: "center" }}
            >
              <img
                src={PenRose}
                alt="Edit"
                style={{ width: 18, height: 18 }}
              />
            </span>
          )}
        </>
      )}
    </OutlineCard>
  );
}
