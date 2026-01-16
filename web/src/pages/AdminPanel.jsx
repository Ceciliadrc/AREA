/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** AdminPanel.jsx
*/

import { PageTitle } from "../components/ui/PageTitle";
import PrimaryButton from "../components/ui/PrimaryButton";
import UsersTable from "../components/admin/UsersTable";
import UserOverlay from "../components/admin/UserOverlay";
import api from "../apiFetcher/api";
import TextButton from "../components/ui/TextButton";
import { colors } from "../components/theme";

export default function AdminPanel({ goTo }) {
  const [users, setUsers] = useState([]);
  const [overlay, setOverlay] = useState({
    open: false,
    mode: null,
    user: null
  });
  const [loading, setLoading] = useState(true);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await api.getUsers();
      setUsers(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load users:", err);
      alert("Failed to load users.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);


  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;

    try {
      await api.deleteUser(id);
      setUsers((prev) => prev.filter((u) => u.id !== id));
    } catch (err) {
      console.error("Failed to delete user:", err);
      alert("Failed to delete user.");
    }
  };

  const handleSave = async (userData) => {
    try {
      if (overlay.mode === "create") {
        // TODO: Implémenter route api pour créer des users
        console.warn("createUser is not implemented in API");
        alert("User creation is not implemented yet.");
        return;
      }

      if (overlay.mode === "edit" && overlay.user?.id) {
        // TODO: Implémenter route api pour edit des users (juste écraser l'ancien et en créer un nouveau à la limite)
        console.warn("updateUser is not implemented in API");
        alert("User update is not implemented yet.");
        return;
      }

      setOverlay({ open: false, mode: null, user: null });
    } catch (err) {
      console.error("Failed to save user:", err);
      alert("Failed to save user.");
    }
  };

  return (
    <AppLayout>
      <div style={{ padding: "60px 40px" }}>
        <PageTitle>Admin panel</PageTitle>

        <TextButton
          onClick={() => goTo && goTo("profile")}
          style={{
            color: "black",
            marginBottom: 20,
            fontSize: 14,
            display: "inline-block"
          }}
        >
          ← Back to profile
        </TextButton>

        <PrimaryButton
          onClick={() =>
            setOverlay({ open: true, mode: "create", user: null })
          }
        >
          + Create user
        </PrimaryButton>

        <br />
        <br />

        <UsersTable
          users={users}
          style={{ color: "black" }}
          onView={(u) => setOverlay({ open: true, mode: "view", user: u })}
          onEdit={(u) => setOverlay({ open: true, mode: "edit", user: u })}
          onDelete={handleDelete}
        />

        {loading && (
          <p style={{ marginTop: 20, color: colors.textMuted }}>
            Loading users…
          </p>
        )}
      </div>

      <UserOverlay
        {...overlay}
        onClose={() =>
          setOverlay({ open: false, mode: null, user: null })
        }
        onSaved={handleSave}
      />
    </AppLayout>
  );
}
