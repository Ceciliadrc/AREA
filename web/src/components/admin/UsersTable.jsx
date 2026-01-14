/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR
** UsersTable.jsx
*/

import PrimaryButton from "../ui/PrimaryButton";

export default function UsersTable({ users, onView, onEdit, onDelete }) {
  return (
    <table
      width="100%"
      style={{
        borderCollapse: "collapse",
        border: "2px solid black",
        backgroundColor: "white",
        color: "black",
      }}
    >
      <thead>
        <tr>
          <Th>Username</Th>
          <Th>Email</Th>
          <Th>Permissions</Th>
          <Th>Actions</Th>
        </tr>
      </thead>

      <tbody>
        {users.map((u) => (
          <tr key={u.id}>
            <Td>{u.username}</Td>
            <Td>{u.email}</Td>
            <Td>
              {u.permissions &&
                Object.entries(u.permissions)
                  .filter(([_, v]) => v)
                  .map(([k]) => k.toUpperCase())
                  .join(", ")}
            </Td>
            <Td>
              <div style={{ display: "flex", gap: 8 }}>
                <PrimaryButton onClick={() => onView(u)}>View</PrimaryButton>
                <PrimaryButton onClick={() => onEdit(u)}>Edit</PrimaryButton>
                <PrimaryButton onClick={() => onDelete(u.id)}>Delete</PrimaryButton>
              </div>
            </Td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const Th = ({ children }) => (
  <th
    style={{
      border: "2px solid black",
      padding: "12px",
      backgroundColor: "#eee",
      textAlign: "left",
    }}
  >
    {children}
  </th>
);

const Td = ({ children }) => (
  <td
    style={{
      border: "1px solid black",
      padding: "12px",
      verticalAlign: "middle",
    }}
  >
    {children}
  </td>
);
