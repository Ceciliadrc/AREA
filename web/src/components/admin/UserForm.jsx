/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR
** UserForm.jsx
*/

import { useEffect, useState } from "react";
import PrimaryButton from "../ui/PrimaryButton";
import TextInput from "../ui/TextInput";
import api from "../../apiFetcher/api";

export default function UserForm({ user, mode, onSaved, onClose }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const [permissions, setPermissions] = useState({
    read: true,
    create: false,
    update: false,
    delete: false,
  });

  useEffect(() => {
    if (user) {
      setUsername(user.username || "");
      setEmail(user.email || "");
      setPermissions(
        user.permissions || {
          read: true,
          create: false,
          update: false,
          delete: false,
        }
      );
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      username,
      email,
      permissions,
    };

    try {
      if (mode === "create") {
        await api.request("users", {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }

      if (mode === "edit") {
        await api.request(`users/${user.id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      }

      onSaved();
      onClose();
    } catch (err) {
      console.warn("API not ready, using mock mode", err);
      onSaved(payload);
      onClose();
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextInput
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        style={{ marginTop: 12, backgroundColor: "white", width: "95%" }}
      />

      <TextInput
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        style={{ marginTop: 12, backgroundColor: "white", width: "95%" }}
      />

      <div style={{ marginTop: 20, color: "black" }}>
        <h3>Permissions</h3>

        {["read", "create", "update", "delete"].map((perm) => (
          <label
            key={perm}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              marginBottom: 6,
            }}
          >
            <input
              type="checkbox"
              checked={permissions[perm]}
              onChange={(e) =>
                setPermissions((prev) => ({
                  ...prev,
                  [perm]: e.target.checked,
                }))
              }
            />
            {perm.toUpperCase()}
          </label>
        ))}
      </div>

      <PrimaryButton type="submit" style={{ marginTop: 16 }}>
        {mode === "create" ? "Create user" : "Save changes"}
      </PrimaryButton>
    </form>
  );
}
