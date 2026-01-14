/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** WorkflowCard.jsx
*/

export default function WorkflowCard({ area, onEdit, onDelete }) {
  return (
    <div
      style={{
        backgroundColor: colors.cardBackground,
        borderRadius: 18,
        padding: "20px 26px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
        border: `1px solid ${colors.border}`,
      }}
    >
      {/* Left side */}
      <div>
        <h3
          style={{
            margin: 0,
            fontSize: 20,
            color: colors.textMain,
            fontWeight: 600,
          }}
        >
          {area.name || "Unnamed workflow"}
        </h3>

        <p
          style={{
            margin: "6px 0 0",
            fontSize: 14,
            color: colors.textMuted,
          }}
        >
          Action #{area.action_id} → Reaction #{area.reaction_id}
        </p>
      </div>

      {/* Right side */}
      <div style={{ display: "flex", gap: 12 }}>
        <IconButton onClick={onEdit}>✏️</IconButton>
        <IconButton danger onClick={onDelete}>🗑️</IconButton>
      </div>
    </div>
  );
}

function IconButton({ children, onClick, danger }) {
  return (
    <button
      onClick={onClick}
      style={{
        width: 42,
        height: 42,
        borderRadius: 12,
        border: "none",
        cursor: "pointer",
        fontSize: 18,
        backgroundColor: danger ? "#ffe5e5" : "#f1e8eb",
        color: danger ? "#d43b3b" : colors.primary,
        transition: "0.15s",
      }}
    >
      {children}
    </button>
  );
}
