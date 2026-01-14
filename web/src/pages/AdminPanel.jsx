/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR
** AdminPanel.jsx
*/

import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import { PageTitle } from "../components/ui/PageTitle";
import PrimaryButton from "../components/ui/PrimaryButton";
import UsersTable from "../components/admin/UsersTable";
import UserOverlay from "../components/admin/UserOverlay";
import api from "../apiFetcher/api";
import TextButton from "../components/ui/TextButton";
import { colors } from "../components/theme";

const MOCK_USERS = [ // TODO: requête api pour get les users
  {
    id: 1,
    username: "admin",
    email: "admin@area.com",
    permissions: { read: true, create: true, update: true, delete: true },
  },
  {
    id: 2,
    username: "user",
    email: "user@area.com",
    permissions: { read: true, create: false, update: false, delete: false },
  },
];

export default function AdminPanel({ goTo }) {
  const [users, setUsers] = useState(MOCK_USERS);
  const [overlay, setOverlay] = useState({ open: false, mode: null, user: null });

  const loadUsers = async () => {
    try {
      const data = await api.request("users");  // TODO: implémenter la route pour les users
      setUsers(data);
    } catch {
      setUsers(MOCK_USERS);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  return (
    <AppLayout>
      <div style={{ padding: "60px 40px" }}>
        <PageTitle>Admin panel</PageTitle>

        <TextButton
          onClick={() => {
            if (goTo) goTo("profile");
          }}
          style={{
            color: "black",
            marginBottom: 20,
            fontSize: 14,
            display: "inline-block"
          }}
        >
          ← Back to profile
        </TextButton>

        <br/>
        <br/>
        <br/>

        <PrimaryButton
          onClick={() => setOverlay({ open: true, mode: "create" })}
        >
          + Create user
        </PrimaryButton>

        <br/>
        <br/>
        <br/>

        <UsersTable
          users={users}
          style={{ color: "black" }}
          onView={(u) => setOverlay({ open: true, mode: "view", user: u })}
          onEdit={(u) => setOverlay({ open: true, mode: "edit", user: u })}
          onDelete={(id) =>
            setUsers((prev) => prev.filter((u) => u.id !== id))
          }
        />
      </div>

      <UserOverlay
        {...overlay}
        onClose={() => setOverlay({ open: false })}
        onSaved={(u) => {
          if (overlay.mode === "create")
            setUsers((prev) => [...prev, { ...u, id: Date.now() }]);
          else
            setUsers((prev) =>
              prev.map((x) => (x.id === overlay.user.id ? { ...x, ...u } : x))
            );
        }}
      />
    </AppLayout>
  );
}
