/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** UserOverlay.jsx
*/

import Overlay from "../ui/Overlay";
import UserForm from "./UserForm";

export default function UserOverlay({ open, mode, user, onClose, onSaved }) {
  return (
    <Overlay isOpen={open} onClose={onClose} width={420}>
      {mode === "view" && user && (
        <>
          <h2 style={{ color: "black" }}>User</h2>
          <p style={{ color: "black" }}>{user.username}</p>
          <p style={{ color: "black" }}>{user.email}</p>
        </>
      )}

      {(mode === "edit" || mode === "create") && (
        <UserForm user={user} mode={mode} onSaved={onSaved} onClose={onClose} />
      )}
    </Overlay>
  );
}
