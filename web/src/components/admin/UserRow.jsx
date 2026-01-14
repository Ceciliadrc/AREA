/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR [WSL: Ubuntu]
** File description:
** UserRow.jsx
*/

export default function UserRow({ user, onView, onEdit, onDelete }) {
  return (
    <tr>
      <td>{user.id}</td>
      <td>{user.username}</td>
      <td>{user.email}</td>
      <td>
        <button onClick={onView}>👁</button>
        <button onClick={onEdit}>✏️</button>
        <button onClick={onDelete}>🗑</button>
      </td>
    </tr>
  );
}
